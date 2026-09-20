import os
import sys
import re
import time
import base64
from pathlib import Path
from typing import List, Optional

# Add api directory to sys.path for robust imports in serverless
CURRENT_DIR = Path(__file__).parent.resolve()
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import edge_tts

from bangla_normalizer import normalize_bangla_for_tts
from knowledge_base import RVL_PROMPT_KNOWLEDGE_TEXT, SYSTEM_VOICE_INSTRUCTIONS

# ── App & Middleware ─────────────────────────────────────────────────────────
app = FastAPI(
    title="Relief Validation Limited (RVL) - AI Voice Studio Serverless API",
    description="Serverless bilingual AI Voice Assistant for RVL, VDS, VeriQR, and OneID",
    version="5.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    env_file = CURRENT_DIR.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("GROQ_API_KEY="):
                GROQ_API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ── Models ──────────────────────────────────────────────────────────────────
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: Optional[str] = "groq/qwen3.8-27b"
    system_prompt: Optional[str] = None
    messages: List[Message]

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "bn-BD-NabanitaNeural"
    rate: Optional[str] = "+8%"
    pitch: Optional[str] = "+0Hz"

class VoiceTurnRequest(BaseModel):
    text: str
    language: Optional[str] = "bn-BD"
    voice: Optional[str] = "bn-BD-NabanitaNeural"
    history: Optional[List[Message]] = []

# ── Utilities ────────────────────────────────────────────────────────────────
def clean_reply(text: str) -> str:
    if not text:
        return ""
    # Strip <think> tags
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Strip markdown symbols
    cleaned = cleaned.replace("**", "").replace("*", "").replace("##", "").replace("#", "")
    return cleaned.strip()

def build_system_prompt(custom_prompt: Optional[str] = None) -> str:
    base = custom_prompt.strip() if custom_prompt else SYSTEM_VOICE_INSTRUCTIONS.strip()
    return f"{base}\n\n{RVL_PROMPT_KNOWLEDGE_TEXT.strip()}"

async def query_groq(model_name: str, messages: list, max_tokens: int = 220) -> str:
    groq_models = {
        "groq/qwen3.8-27b": "qwen/qwen3.8-27b",
        "groq/gpt-oss-20b": "openai/gpt-oss-20b",
        "qwen/qwen3.8-27b": "qwen/qwen3.8-27b",
        "openai/gpt-oss-20b": "openai/gpt-oss-20b"
    }
    target_model = groq_models.get(model_name, "qwen/qwen3.8-27b")

    payload = {
        "model": target_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.5
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(GROQ_URL, json=payload, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            raw = data["choices"][0]["message"].get("content", "")
            return clean_reply(raw)
        else:
            raise HTTPException(status_code=resp.status_code, detail=f"Groq API Error: {resp.text}")

async def synthesize_speech_in_memory(text: str, voice: str, rate: str = "+8%", pitch: str = "+0Hz") -> bytes:
    # Phonetic normalizer for Bangla pronunciation
    spoken_text = normalize_bangla_for_tts(text)

    # Auto detect Bangla
    has_bangla = bool(re.search(r'[\u0980-\u09FF]', text))
    if not voice or voice == "auto":
        voice = "bn-BD-NabanitaNeural" if has_bangla else "en-IN-NeerjaNeural"
    elif has_bangla and not voice.startswith("bn-"):
        voice = "bn-BD-NabanitaNeural"

    communicate = edge_tts.Communicate(spoken_text, voice=voice, rate=rate, pitch=pitch)
    audio_buffer = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.extend(chunk["data"])

    return bytes(audio_buffer)

# ── Endpoints ────────────────────────────────────────────────────────────────
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "RVL Voice Studio Serverless",
        "environment": "Vercel / Cloud Edge",
        "timestamp": int(time.time())
    }

@app.get("/api/config")
async def get_config():
    return {
        "status": "ready",
        "company": "Relief Validation Limited (RVL)",
        "license": "Licensed CA under ICT Act 2006 (CCA Bangladesh)",
        "models": [
            {"id": "groq/qwen3.8-27b", "name": "Groq Qwen 2.5 (Sub-400ms Ultra Fast)", "provider": "Groq LPU"},
            {"id": "groq/gpt-oss-20b", "name": "Groq GPT-OSS 20B (High Reasoning)", "provider": "Groq LPU"}
        ],
        "voices": [
            {"id": "bn-BD-NabanitaNeural", "name": "Nabanita (Dhaka Female - Natural)", "lang": "bn-BD"},
            {"id": "bn-BD-PradeepNeural", "name": "Pradeep (Dhaka Male - Professional)", "lang": "bn-BD"},
            {"id": "en-IN-NeerjaNeural", "name": "Neerja (English - Corporate)", "lang": "en-US"}
        ],
        "knowledge_base": RVL_PROMPT_KNOWLEDGE_TEXT.strip()
    }

@app.post("/api/chat")
async def chat(req: ChatRequest):
    t0 = time.time()
    system_prompt = build_system_prompt(req.system_prompt)

    messages = [{"role": "system", "content": system_prompt}]
    for m in req.messages:
        if m.role in ["user", "assistant"]:
            messages.append({"role": m.role, "content": m.content})

    reply = await query_groq(req.model, messages, max_tokens=220)
    latency_ms = int((time.time() - t0) * 1000)

    return {
        "reply": reply,
        "provider": f"groq_cloud",
        "latency_ms": latency_ms
    }

@app.post("/api/tts")
async def text_to_speech(req: TTSRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    audio_bytes = await synthesize_speech_in_memory(
        text=req.text,
        voice=req.voice or "bn-BD-NabanitaNeural",
        rate=req.rate or "+8%",
        pitch=req.pitch or "+0Hz"
    )

    return Response(content=audio_bytes, media_type="audio/mpeg")

@app.post("/api/voice/turn")
async def voice_turn(req: VoiceTurnRequest):
    """
    Combined voice turn for low mobile latency:
    Takes user speech, queries LLM, generates TTS audio, returns both in ONE roundtrip!
    """
    t0 = time.time()
    system_prompt = build_system_prompt()

    messages = [{"role": "system", "content": system_prompt}]
    if req.history:
        for m in req.history:
            if m.role in ["user", "assistant"]:
                messages.append({"role": m.role, "content": m.content})
    messages.append({"role": "user", "content": req.text})

    reply = await query_groq("groq/qwen3.8-27b", messages, max_tokens=220)

    # Generate TTS
    voice = req.voice or ("bn-BD-NabanitaNeural" if req.language == "bn-BD" else "en-IN-NeerjaNeural")
    audio_bytes = await synthesize_speech_in_memory(reply, voice=voice)
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    latency_ms = int((time.time() - t0) * 1000)
    return {
        "user_text": req.text,
        "reply": reply,
        "audio_base64": audio_b64,
        "format": "audio/mp3",
        "latency_ms": latency_ms
    }

@app.post("/v1/chat/completions")
async def openai_compatible_chat(request: Request):
    data = await request.json()
    model_id = data.get("model", "qwen/qwen3.8-27b")
    messages = data.get("messages", [])

    # Prepend knowledge
    system_prompt = build_system_prompt()
    formatted = [{"role": "system", "content": system_prompt}]
    for m in messages:
        if m.get("role") in ["user", "assistant"]:
            formatted.append({"role": m["role"], "content": m["content"]})

    reply = await query_groq(model_id, formatted, max_tokens=data.get("max_tokens", 220))

    return {
        "id": f"chatcmpl-rvl-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model_id,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": reply
            },
            "finish_reason": "stop"
        }]
    }
