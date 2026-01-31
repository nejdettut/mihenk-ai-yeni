import os
import io
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.services.storage_service import StorageService

class ReportService:
    @staticmethod
    async def generate_report(analysis_result: dict) -> str:
        """Generates a simple PDF report and returns a URL to it.
        - In TEST_MODE, writes file locally to backend/tmp/reports and returns a file:// path
        - Otherwise uploads PDF to Supabase storage under bucket 'reports' and returns public URL
        """
        # Create PDF in-memory
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Title
        c.setFont("Helvetica-Bold", 18)
        c.drawString(40, height - 60, "Mihenk.ai - Sınav Analiz Raporu")

        # Score
        c.setFont("Helvetica-Bold", 14)
        score = analysis_result.get("toplam_puan") or analysis_result.get("total_score") or "N/A"
        c.drawString(40, height - 100, f"Toplam Puan: {score}")

        # Teacher note
        c.setFont("Helvetica", 12)
        teacher_note = analysis_result.get("ogretmen_notu", "")
        c.drawString(40, height - 130, f"Öğretmen Notu: {teacher_note}")

        # Simple question-by-question summary (first 10 items max)
        qa = analysis_result.get("soru_bazli_analiz", []) or analysis_result.get("soru_analiz", []) or []
        y = height - 170
        c.setFont("Helvetica", 11)
        for i, q in enumerate(qa[:10], start=1):
            q_text = f"{i}. {q.get('soru') if isinstance(q, dict) else str(q)}"
            c.drawString(40, y, q_text[:100])
            y -= 16
            if y < 80:
                c.showPage()
                y = height - 60

        c.showPage()
        c.save()
        buffer.seek(0)
        pdf_bytes = buffer.read()

        # File name
        file_name = f"report_{uuid.uuid4()}.pdf"

        # TEST_MODE local write
        if os.getenv("TEST_MODE") == "1":
            local_dir = os.path.join(os.getcwd(), "tmp", "reports")
            os.makedirs(local_dir, exist_ok=True)
            local_path = os.path.join(local_dir, file_name)
            with open(local_path, "wb") as f:
                f.write(pdf_bytes)
            # Return a backend-served path so frontend can fetch it via HTTP
            return f"/api/v1/reports/public/{file_name}"

        # Upload to Supabase storage bucket 'reports'
        url = await StorageService.upload_file(pdf_bytes, file_name, bucket="reports")
        return url
