import os
import sys
import re
import time
import base64
import io
from pathlib import Path
from typing import List, Optional

# Add api directory to sys.path for robust imports in serverless
CURRENT_DIR = Path(__file__).parent.resolve()
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from fastapi import FastAPI, HTTPException, Request, Response, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import edge_tts

from bangla_normalizer import normalize_bangla_for_tts
from knowledge_base import RVL_PROMPT_KNOWLEDGE_TEXT, SYSTEM_VOICE_INSTRUCTIONS, get_smart_fallback

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

    # Extract last user query for smart fallback
    last_user_query = ""
    for m in reversed(messages):
        if isinstance(m, dict) and m.get("role") == "user":
            last_user_query = m.get("content", "")
            break
        elif hasattr(m, "role") and m.role == "user":
            last_user_query = m.content
            break

    has_bangla = bool(re.search(r'[\u0980-\u09FF]', last_user_query))
    lang = "bn" if has_bangla else "en"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    # Strategy 1: Candidate models cascade
    candidate_models = [target_model, "llama-3.1-8b-instant"]
    for cand in candidate_models:
        payload = {
            "model": cand,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.5
        }
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.post(GROQ_URL, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    raw = data["choices"][0]["message"].get("content", "")
                    cleaned = clean_reply(raw)
                    if cleaned and len(cleaned) > 10:
                        return cleaned
        except Exception as e:
            print(f"[Groq Attempt Failed for {cand}]: {e}", flush=True)

    # Strategy 2: Instant Smart Corporate Knowledge Matcher
    return get_smart_fallback(last_user_query, lang=lang)

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

@app.post("/api/stt")
async def speech_to_text(
    audio: UploadFile = File(...),
    language: str = Form(default="bn")
):
    """
    Mobile STT endpoint: Receives audio blob from MediaRecorder (webm/mp4/ogg),
    sends to Groq Whisper large-v3, returns transcribed text.
    Supports Bangla (bn) and English (en).
    """
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    try:
        audio_bytes = await audio.read()
        if not audio_bytes or len(audio_bytes) < 500:
            return {"text": "", "language": language, "error": "Audio too short or empty"}

        # Determine MIME type from upload
        content_type = audio.content_type or "audio/webm"
        filename = audio.filename or "audio.webm"
        if "mp4" in content_type or "mp4" in filename:
            mime = "audio/mp4"
            ext = "mp4"
        elif "ogg" in content_type or "ogg" in filename:
            mime = "audio/ogg"
            ext = "ogg"
        elif "wav" in content_type or "wav" in filename:
            mime = "audio/wav"
            ext = "wav"
        elif "mpeg" in content_type or "mp3" in filename:
            mime = "audio/mpeg"
            ext = "mp3"
        else:
            mime = "audio/webm"
            ext = "webm"

        # Groq Whisper transcription endpoint
        groq_whisper_url = "https://api.groq.com/openai/v1/audio/transcriptions"
        headers_whisper = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }

        # Groq Whisper language codes: "bn" for Bangla, "en" for English
        whisper_lang = "bn" if language in ["bn-BD", "bn", "bangla"] else "en"

        files_data = {
            "file": (f"audio.{ext}", io.BytesIO(audio_bytes), mime),
            "model": (None, "whisper-large-v3"),
            "language": (None, whisper_lang),
            "response_format": (None, "json"),
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(groq_whisper_url, headers=headers_whisper, files=files_data)

        if resp.status_code == 200:
            data = resp.json()
            transcribed = data.get("text", "").strip()
            return {"text": transcribed, "language": whisper_lang, "chars": len(transcribed)}
        else:
            print(f"[Whisper STT Error] {resp.status_code}: {resp.text[:200]}", flush=True)
            return {"text": "", "language": whisper_lang, "error": f"Whisper API error {resp.status_code}"}

    except Exception as e:
        print(f"[STT Exception] {e}", flush=True)
        return {"text": "", "error": str(e)}


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
