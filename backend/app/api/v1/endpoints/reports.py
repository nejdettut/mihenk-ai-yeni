from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
import os

router = APIRouter()

@router.get("/public/{file_name}")
async def get_report(file_name: str):
    """Serve report files in TEST_MODE from backend tmp/reports, otherwise redirect to public URL"""
    if os.getenv("TEST_MODE") == "1":
        local_path = os.path.join(os.getcwd(), "tmp", "reports", file_name)
        if not os.path.exists(local_path):
            raise HTTPException(status_code=404, detail="Report not found")
        return FileResponse(local_path, media_type="application/pdf", filename=file_name)

    # In production the ReportService would return a public URL (hosted on storage)
    # For safety, return 404 here when not in test mode
    raise HTTPException(status_code=404, detail="Report serving not available in production; use report URL from DB")
