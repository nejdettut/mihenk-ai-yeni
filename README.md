# Mihenk AI

Lightweight exam-analysis platform (FastAPI backend, Next.js frontend).

Quick start (development):

1. Backend
```bash
cd backend
python -m venv .venv
. .venv/Scripts/Activate.ps1  # Windows PowerShell
pip install -r requirements.txt# Note: if you plan to use RAG endpoints with document extraction, install textract manually
# as it can fail to build on some platforms: `pip install textract`cp .env.example .env
# edit .env to set keys (or set TEST_MODE=1 for local testing)
uvicorn app.main:app --reload --port 8001
```

2. Frontend
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Set NEXT_PUBLIC_API_BASE to backend URL (e.g. http://localhost:8001)
npm run dev
```

Deploy hints
- Frontend: Vercel (connect repo, set `NEXT_PUBLIC_API_BASE` env var)
- Backend: Render / Railway / Fly / Cloud Run (Dockerfile included)
- Database & Storage: Supabase

Repository setup
- Add secrets to your chosen platform (SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY, STRIPE_SECRET_KEY)

Contributing
- Clean temporary files before commit; see .gitignore
