from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID

# --- BASE MODELLER ---

class ProfileBase(BaseModel):
    full_name: str
    school_name: Optional[str] = None
    subscription_tier: str = "free"

class ClassBase(BaseModel):
    name: str
    grade_level: Optional[int] = None

class StudentBase(BaseModel):
    student_number: str
    full_name: str
    class_id: UUID

class ExamBase(BaseModel):
    title: str
    answer_key: dict  # Soru-cevap eşleşmeleri
    max_score: int = 100
    class_id: UUID

# --- API İÇİN OLUŞTURMA (CREATE) MODELLERİ ---
# ID ve Tarih gibi sistemin atayacağı alanlar burada yer almaz.

class ClassCreate(ClassBase):
    pass

class StudentCreate(StudentBase):
    pass

class ExamCreate(ExamBase):
    pass

# --- API'DEN DÖNECEK (RESPONSE) MODELLERİ ---
# Veritabanından veri çekerken bu modelleri kullanacağız.

class StudentResponse(StudentBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ClassResponse(ClassBase):
    id: UUID
    teacher_id: UUID
    students: List[StudentResponse] = [] # İlişkili öğrencileri de görebiliriz

    class Config:
        from_attributes = True

# --- ANALİZ SONUCU MODELİ ---

class ExamResultResponse(BaseModel):
    id: UUID
    exam_id: UUID
    student_id: UUID
    paper_image_url: str
    total_score: float
    feedback_json: dict
    created_at: datetime

    class Config:
        from_attributes = True
