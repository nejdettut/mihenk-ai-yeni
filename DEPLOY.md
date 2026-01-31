# Deploy Guide

Frontend (Vercel)
1. Connect your GitHub repo to Vercel.
2. In Vercel project settings, set environment variables:
   - NEXT_PUBLIC_API_BASE = https://your-backend-url
3. Deploy — Vercel will build and host the Next.js site.

Backend (Render / Railway / Fly / Cloud Run)
1. Create a new Web Service (Docker/Build from repo).
2. Use `backend/Dockerfile` or set start command:
   `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables (SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY, STRIPE_SECRET_KEY, etc.)

Supabase
- If you use Supabase for DB/storage, paste keys into backend env.

Local testing
- Set backend `TEST_MODE=1` in `backend/.env` to run without external services.

GitHub
- Push your local repo to GitHub:
  1. Create repo on GitHub
  2. git remote add origin git@github.com:youruser/yourrepo.git
  3. git push -u origin main
