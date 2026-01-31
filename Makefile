.PHONY: dev-backend dev-frontend install

dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8001

dev-frontend:
	cd frontend && npm run dev

install:
	python -m venv .venv && . .venv/Scripts/Activate.ps1 && pip install -r backend/requirements.txt && cd frontend && npm install
