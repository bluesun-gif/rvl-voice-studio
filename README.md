# 🎙️ Relief Validation Limited (RVL) — Cloud AI Voice Studio

A production-ready, ultra-low-latency, bilingual (**Bangla & English**) AI Voice Assistant for **Relief Validation Limited (RVL)**, **DGePay Services Limited**, and **Deepon Group**.

---

## 🚀 Key Advantages of this Vercel Deployment

1. **Zero VPS Required**: 100% serverless on Vercel's global edge network. No monthly server bills, no Linux management, no maintenance.
2. **Laptop Can Be Turned Off**: Runs 24/7/365 in the cloud. Anyone anywhere in the world (including the CEO, board members, and bank executives) can test and use it anytime.
3. **Worldwide HTTPS Out of the Box**: Mobile browsers (iOS Safari, Android Chrome) strictly block microphone access on insecure HTTP. Vercel automatically provides enterprise SSL certificates for free.
4. **Sub-Second Latency**:
   - **STT (Speech-to-Text)**: Runs in-browser via Web Speech API or cloud Whisper.
   - **LLM Brain**: Groq Cloud LPU (`llama-3.3-70b` / `qwen-2.5-32b`) generating replies in ~250–400ms.
   - **TTS Voice**: Microsoft Edge Neural TTS streaming Bengali (`bn-BD-NabanitaNeural`) in-memory.
   - **Bangla Phonetics**: English acronyms (`VDS`, `VeriQR`, `OneID`, `ICT Act`) are automatically normalized to native Bengali phonetics (`ভি ডি এস`, `ভেরি কিউআর`, `ওয়ানআইডি`).

---

## 📦 Project Structure

```
rvl_voice_studio_vercel/
├── api/
│   ├── index.py              # FastAPI Serverless Handler
│   ├── bangla_normalizer.py   # Phonetic dictionary for Dhaka Bengali TTS
│   └── knowledge_base.py     # Master RVL, VDS, VeriQR, and Deepon knowledge
├── public/
│   └── index.html            # Web Audio VU meter, 1-click language switch, Echo-Lock UI
├── .env.example              # Environment variables template
├── requirements.txt          # Lightweight Python serverless dependencies
├── vercel.json               # Vercel serverless routing rules
└── README.md
```

---

## 🛠️ How to Deploy to Vercel (2 Methods)

### Method 1: Deploy with GitHub (Recommended & 1-Click)
1. Initialize git and push this folder to your GitHub:
   ```bash
   git init
   git add .
   git commit -m "RVL Voice Studio for Vercel"
   git branch -M main
   git remote add origin https://github.com/<your-username>/rvl-voice-studio.git
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com) and click **"Add New Project"** -> **"Import Git Repository"**.
3. Select `rvl-voice-studio`.
4. In **Environment Variables**, add:
   - `GROQ_API_KEY`: `your_groq_api_key`
5. Click **"Deploy"**.
6. In ~45 seconds, Vercel gives you your live public link:
   👉 `https://rvl-voice-studio.vercel.app`

### Method 2: Deploy directly via Vercel CLI
1. Open PowerShell in this folder:
   ```powershell
   cd c:\Users\LOQ\.hermes\rvl_voice_studio_vercel
   ```
2. Run:
   ```powershell
   npx vercel
   ```
3. Follow the quick terminal prompts (log in with your Vercel account).
4. Add your Groq API key:
   ```powershell
   npx vercel env add GROQ_API_KEY production
   npx vercel --prod
   ```

---

## 🌐 Adding a Custom Domain (e.g. `voice.toolzium.com`)
1. In your Vercel Dashboard, go to **Settings** -> **Domains**.
2. Type `voice.toolzium.com` (or `voice.reliefvalidation.com.bd`).
3. Add the CNAME record in your DNS provider (Cloudflare) pointing to `cname.vercel-dns.com`.
4. Vercel automatically generates the SSL certificate within 60 seconds!
