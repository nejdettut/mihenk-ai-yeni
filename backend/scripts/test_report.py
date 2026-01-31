import sys
from pathlib import Path
# Ensure backend package imports work when running script from repo root
backend_root = str(Path(__file__).resolve().parents[1])
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

import os
# Ensure env vars exist so pydantic Settings doesn't crash during local tests
# Provide dummy non-empty values so client initialization won't fail during local tests
os.environ.setdefault('SUPABASE_URL', 'http://localhost')
os.environ.setdefault('SUPABASE_KEY', 'test')
os.environ.setdefault('GEMINI_API_KEY', 'test')
os.environ.setdefault('GROQ_API_KEY', 'test')

import asyncio
from app.services.report_service import ReportService

async def run():
    fake = {
        "toplam_puan": 88,
        "soru_bazli_analiz": [{"soru": "1: doğru"}, {"soru": "2: yanlış"}],
        "ogretmen_notu": "Test raporu"
    }
    url = await ReportService.generate_report(fake)
    print('Report URL:', url)

if __name__ == '__main__':
    asyncio.run(run())
