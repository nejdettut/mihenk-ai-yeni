import os
import json
import asyncio
from typing import List, Dict
from pathlib import Path
import hashlib

# NOTE: This is a lightweight RAG service suitable for local/test mode.
# For production, replace storage with SupabaseVectorStore (pgvector) + proper embeddings (OpenAI / Google).

KB_ROOT = Path(os.getcwd()) / "tmp" / "knowledge_base"
KB_ROOT.mkdir(parents=True, exist_ok=True)


def _simple_embed(text: str) -> List[float]:
    # Deterministic stub embedding: hash the text and create small vector.
    h = hashlib.sha256(text.encode("utf-8")).digest()
    vec = [((b % 128) - 64) / 64.0 for b in h[:32]]
    return vec


class RAGService:
    @staticmethod
    async def add_document_to_knowledge_base(content: str, metadata: dict, class_id: str):
        """Split document into simple chunks, create embeddings and store in local KB (test mode).
        metadata can include 'source', 'title', 'page' etc.
        In production, implement SupabaseVectorStore upsert here.
        """
        kb_file = KB_ROOT / f"{class_id}.json"
        if kb_file.exists():
            kb = json.loads(kb_file.read_text())
        else:
            kb = []

        # Naive splitter by paragraphs
        chunks = [p.strip() for p in content.split("\n\n") if p.strip()]
        for i, chunk in enumerate(chunks):
            entry = {
                "id": f"{hashlib.md5((chunk[:64] + str(i)).encode()).hexdigest()}",
                "text": chunk,
                "metadata": metadata,
                "embedding": _simple_embed(chunk),
            }
            kb.append(entry)

        kb_file.write_text(json.dumps(kb, ensure_ascii=False, indent=2))
        return {"status": "ok", "chunks_added": len(chunks)}

    @staticmethod
    async def ask_question_from_docs(query: str, class_id: str, top_k: int = 4) -> Dict:
        """Retrieve top_k chunks from the local KB by cosine similarity and return concatenated context.
        In production, perform a vector similarity query on Supabase (pgvector) and then call a model for final answer.
        """
        kb_file = KB_ROOT / f"{class_id}.json"
        if not kb_file.exists():
            return {"error": "No knowledge base for this class"}

        kb = json.loads(kb_file.read_text())

        q_emb = _simple_embed(query)

        def cosine(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(x * x for x in b) ** 0.5
            if norm_a == 0 or norm_b == 0:
                return 0
            return dot / (norm_a * norm_b)

        scores = [(cosine(q_emb, entry["embedding"]), entry) for entry in kb]
        scores.sort(key=lambda x: x[0], reverse=True)
        top = [s[1] for s in scores[:top_k]]

        # Build a simple synthesized answer (placeholder for LLM call)
        context = "\n\n".join([t["text"] for t in top])
        answer = {
            "query": query,
            "top_k": top_k,
            "results": [{"score": float(s[0]), "metadata": s[1]["metadata"], "text": s[1]["text"]} for s in scores[:top_k]],
            "synthesized_answer": f"Based on {len(top)} document chunks, possible answer: (see context)\n\n{context[:1000]}",
        }
        return answer
