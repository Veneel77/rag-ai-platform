from fastapi import FastAPI
from pydantic import BaseModel
from src.ingestion import load_documents
from src.embed_store import ingest_documents, get_embedder, create_chroma_client
from src.retriever import retrieve_similar
from src.generator import get_generator, generate_answer
import numpy as np

app = FastAPI(title="RAG-AI-PLATFORM for enterprises (local)")

class Query(BaseModel):
    question: str

# lazy init
COLLECTION = None
EMBEDDER = None
GEN = None

@app.on_event("startup")
def startup():
    global COLLECTION, EMBEDDER, GEN
    EMBEDDER = get_embedder()
    client = create_chroma_client()
    docs = load_documents("data")
    if docs:
        COLLECTION = ingest_documents(docs, client)
    else:
        COLLECTION = client.create_collection("enterprise_docs")
    # load generator (may take time)
    GEN = get_generator()

@app.post("/query")
def query(q: Query):
    global COLLECTION, EMBEDDER, GEN
    q_emb = EMBEDDER.encode(q.question)
    res = retrieve_similar(COLLECTION, q_emb, k=4)
    context_docs = "\n\n---\n\n".join([d for d in res["documents"][0]])
    prompt = f"""You are an enterprise assistant. Use the context below to answer the question concisely.\n\nContext:\n{context_docs}\n\nQuestion:\n{q.question}\n\nAnswer:\n"""
    answer = generate_answer(GEN, prompt, max_tokens=512)
    return {"answer": answer, "sources": res["metadatas"][0] if "metadatas" in res else []}
