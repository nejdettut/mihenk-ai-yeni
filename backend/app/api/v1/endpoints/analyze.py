from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.ai_engine import MihenkEngine
from app.services.storage_service import StorageService
from app.services.report_service import ReportService
from app.core.config import supabase
import uuid
import json

router = APIRouter()
ai_engine = MihenkEngine()

@router.post("/full-analysis")
async def start_analysis(
    exam_id: str = Form(...),
    student_id: str = Form(...),
    file: UploadFile = File(...)
):
    """Uçtan uca analiz orkestrasyonu:
    1) Sınav kağıdını Supabase Storage'a yükle
    2) Sınavın cevap anahtarını DB'den al
    3) AI (Gemini + Groq) ile analiz et
    4) Sonucu DB'ye kaydet ve rapor URL'si döndür
    """
    try:
        # 1. Dosyayı oku
        content = await file.read()

        # TEST MODE: dış servisleri çağırmadan hızlıca başarılı cevap dön
        import os
        if os.getenv("TEST_MODE") == "1":
            fake_result = {
                "toplam_puan": 92,
                "soru_bazli_analiz": [],
                "ogretmen_notu": "Test modu: otomatik geri bildirim",
            }
            report_url = ""
            if os.getenv("TEST_MODE_GEN_REPORT") == "1":
                # create a report file in test mode
                report_url = await ReportService.generate_report(fake_result)

            return {
                "message": "Analiz tamamlandı (test modu)",
                "score": fake_result["toplam_puan"],
                "report_url": report_url,
                "analysis": fake_result,
            }

        # 2. Dosyayı Supabase Storage'a yükle
        file_ext = file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        public_url = await StorageService.upload_exam_photo(content, file_name)

        # 3. Sınav bilgilerini DB'den getir (Cevap Anahtarı için)
        exam_data = supabase.table("exams").select("*").eq("id", exam_id).single().execute()
        if exam_data.error:
            raise HTTPException(status_code=404, detail="Exam not found")

        answer_key = exam_data.data.get("answer_key")
        if isinstance(answer_key, str):
            try:
                answer_key = json.loads(answer_key)
            except Exception:
                # leave as-is if not JSON
                pass

        # 4. AI Hibrit Analizi Başlat (Gemini + Groq)
        analysis_result = await ai_engine.analiz_et(content, answer_key)

        # 5. Veritabanına Sonucu Kaydet
        db_data = {
            "exam_id": exam_id,
            "student_id": student_id,
            "paper_image_url": public_url,
            "total_score": analysis_result.get("toplam_puan"),
            "feedback_json": analysis_result,
            "raw_ai_response": analysis_result
        }
        supabase.table("exam_results").insert(db_data).execute()

        # (Opsiyonel) Rapor üretimi
        report_url = await ReportService.generate_report(analysis_result)
        if not report_url:
            report_url = public_url

        return {
            "message": "Analiz tamamlandı",
            "score": analysis_result.get("toplam_puan"),
            "report_url": report_url
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

