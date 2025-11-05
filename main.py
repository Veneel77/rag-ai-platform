from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
from pathlib import Path
import shutil
import os

from src.ingestion import load_documents
from src.embed_store import ingest_documents, get_embedder, create_chroma_client
from src.retriever import retrieve_similar
from src.generator import get_generator, generate_answer


app = FastAPI(title="RAG-AI-PLATFORM for enterprises (local)")

# ----------- MODELS -----------
class Query(BaseModel):
    question: str


# ----------- GLOBALS -----------
COLLECTION = None
EMBEDDER = None
GEN = None
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


# ----------- STARTUP EVENT -----------
@app.on_event("startup")
def startup():
    global COLLECTION, EMBEDDER, GEN
    print("🔹 Initializing embedder and generator...")

    EMBEDDER = get_embedder()
    client = create_chroma_client()

    print("🔹 Loading existing documents...")
    docs = load_documents(DATA_DIR)
    if docs:
        COLLECTION = ingest_documents(docs, client)
        print(f"✅ {len(docs)} documents ingested.")
    else:
        COLLECTION = client.create_collection("enterprise_docs")
        print("⚠️ No documents found, created empty collection.")

    GEN = get_generator()
    print("✅ Generator ready.")


# ----------- INGESTION ENDPOINT -----------
@app.post("/ingest")
async def ingest(files: List[UploadFile] = File(...)):
    """Upload and embed documents into vector store"""
    saved_files = []
    for file in files:
        file_path = Path(DATA_DIR) / file.filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved_files.append(file_path)

    docs = load_documents(DATA_DIR)
    if not docs:
        return {"status": "failed", "message": "No readable documents found."}

    client = create_chroma_client()
    ingest_documents(docs, client)
    return {"status": "success", "message": f"{len(docs)} documents ingested successfully."}


# ----------- QUERY ENDPOINT -----------
@app.post("/query")
def query(q: Query):
    global COLLECTION, EMBEDDER, GEN

    q_emb = EMBEDDER.encode(q.question)
    res = retrieve_similar(COLLECTION, q_emb, k=3)  # keep k=3 for shorter prompt

    # join retrieved chunks
    context_docs = "\n\n---\n\n".join([d for d in res["documents"][0]]) if res and "documents" in res else ""

    # handle empty context
    if not context_docs.strip():
        return {"answer": "No relevant context found in the ingested documents.", "sources": []}

    # truncate context to prevent model overflow
    if len(context_docs) > 6000:
        context_docs = context_docs[:6000]

    prompt = f"""
You are an intelligent enterprise assistant. Use the context below to answer the question concisely.

Context:
{context_docs}

Question:
{q.question}

Answer:
"""
    try:
        answer = generate_answer(GEN, prompt, max_tokens=512)
        sources = res["metadatas"][0] if "metadatas" in res else []
        return {"answer": answer, "sources": sources}
    except Exception as e:
        return {"answer": f"⚠️ Error generating response: {str(e)}", "sources": []}


# ----------- MAIN ENTRY -----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
