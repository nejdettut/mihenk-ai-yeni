from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.rag_service import RAGService
import uuid
import io
import textract

router = APIRouter()

@router.post('/upload')
async def upload_doc(class_id: str = Form(...), file: UploadFile = File(...)):
    # Read bytes
    content_bytes = await file.read()
    # Try extracting text (textract supports many formats)
    try:
        text = textract.process(io.BytesIO(content_bytes), extension=file.filename.split('.')[-1]).decode('utf-8')
    except Exception:
        # fallback: try decode
        try:
            text = content_bytes.decode('utf-8')
        except Exception:
            raise HTTPException(status_code=400, detail='Could not extract text from file')

    metadata = {"source": file.filename}
    result = await RAGService.add_document_to_knowledge_base(text, metadata, class_id)
    return result

@router.post('/query')
async def query_docs(class_id: str = Form(...), query: str = Form(...)):
    result = await RAGService.ask_question_from_docs(query, class_id)
    return result
