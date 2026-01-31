from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import ClassCreate, ClassResponse
from app.services.db_service import DBService
from typing import List

router = APIRouter()

# Şimdilik teacher_id'yi manuel alıyoruz, Auth aşamasında token'dan çekeceğiz.
@router.post("/", response_model=List[ClassResponse])
async def create_new_class(teacher_id: str, class_in: ClassCreate):
    new_class = await DBService.create_class(teacher_id, class_in)
    if not new_class:
        raise HTTPException(status_code=400, detail="Sınıf oluşturulamadı.")
    return new_class

@router.get("/{teacher_id}", response_model=List[ClassResponse])
async def get_classes(teacher_id: str):
    return await DBService.get_teacher_classes(teacher_id)
