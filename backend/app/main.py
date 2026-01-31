from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import classes, analyze

app = FastAPI(title="Mihenk.ai API", version="0.1.0")

# CORS: Frontend (Next.js) için lokal origin izinleri
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route'ları dahil etme
app.include_router(classes.router, prefix="/api/v1/classes", tags=["Classes"])
# AI analiz endpoint'leri öğretmenin beklediği path ile hizalanıyor
app.include_router(analyze.router, prefix="/api/v1/analyze", tags=["AI Analysis"])
app.include_router(__import__('app.api.v1.endpoints.reports', fromlist=['router']).router, prefix="/api/v1/reports", tags=["Reports"])
# RAG (NotebookLM) endpoints
from app.api.v1.endpoints import rag as rag_module
app.include_router(rag_module.router, prefix="/api/v1/rag", tags=["RAG"])

@app.get("/")
async def root():
    return {"message": "Mihenk.ai Backend Aktif!", "status": "Ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
