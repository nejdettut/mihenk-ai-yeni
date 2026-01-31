import google.generativeai as genai
from groq import Groq
from app.core.config import settings
import json

class MihenkEngine:
    def __init__(self):
        # Gemini (Multimodal - Görüntü İşleme için)
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Groq (Hızlı Metin Analizi için)
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)

    async def analiz_et(self, image_bytes: bytes, answer_key: dict):
        """
        1. Adım: Gemini ile görüntüyü metne çevir ve ham analizi al.
        2. Adım: Groq ile analizi rafine et, puanlamayı kontrol et ve JSON'u mükemmelleştir.
        """
        
        # 1. GEMINI: GÖRSEL ANALİZ
        gemini_prompt = f"""
        Sen uzman bir öğretmensin. Sınav kağıdını OCR yaparak oku.
        Cevap Anahtarı: {json.dumps(answer_key)}
        Görseldeki cevapları bu anahtarla kıyasla.
        Her soru için; öğrencinin cevabı, doğruluk durumu ve puanı belirle.
        Çıktıyı sadece JSON olarak ver.
        """
        
        image_part = {"mime_type": "image/jpeg", "data": image_bytes}
        
        # Run synchronous Gemini call in a thread pool if needed, but for now simple call is fine as per request
        # However, generate_content is blocking. Best practice in async FastAPI is to offload blocking calls.
        # But per user request I will implement as is, or slightly optimized if obvious. 
        # User provided code uses self.gemini_model.generate_content which is synchronous.
        # I'll keep it simple as requested.
        gemini_response = self.gemini_model.generate_content([gemini_prompt, image_part])
        raw_text = gemini_response.text

        # 2. GROQ: HIZLI RAFİNERİ VE FEEDBACK
        groq_prompt = f"""
        Aşağıdaki ham sınav verisini al ve öğrenciye özel çok daha motive edici, 
        pedagojik bir geri bildirim ekle. Puan hesaplamasını kontrol et.
        
        Veri: {raw_text}
        
        Format:
        {{
            "toplam_puan": 0,
            "soru_bazli_analiz": [],
            "ogretmen_notu": "Groq tarafından optimize edilmiş pedagojik not"
        }}
        """
        
        # Groq client is also sync by default unless AsyncGroq is used. 
        # User initialized Groq() which is sync. I will follow user's code but note that async would be better.
        groq_chat = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": groq_prompt}],
            model="llama3-70b-8192", # En güçlü ve hızlı model
            response_format={"type": "json_object"}
        )
        
        return json.loads(groq_chat.choices[0].message.content)
