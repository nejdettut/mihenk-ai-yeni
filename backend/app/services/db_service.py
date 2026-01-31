from app.core.config import supabase
from app.models.schemas import ClassCreate, StudentCreate
from uuid import UUID

class DBService:
    @staticmethod
    async def create_class(teacher_id: str, class_data: ClassCreate):
        # Sınıf oluşturma
        data = {
            "teacher_id": teacher_id,
            "name": class_data.name,
            "grade_level": class_data.grade_level
        }
        # Supabase-py sync client executed within async function
        response = supabase.table("classes").insert(data).execute()
        return response.data

    @staticmethod
    async def get_teacher_classes(teacher_id: str):
        # Öğretmenin tüm sınıflarını listeleme
        response = supabase.table("classes").select("*").eq("teacher_id", teacher_id).execute()
        return response.data

    @staticmethod
    async def add_student(student_data: StudentCreate):
        # Sınıfa öğrenci ekleme
        data = student_data.model_dump()
        response = supabase.table("students").insert(data).execute()
        return response.data
