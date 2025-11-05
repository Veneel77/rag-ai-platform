from sentence_transformers import SentenceTransformer

import os

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def get_embedder():
    model = SentenceTransformer(EMBED_MODEL)
    return model


import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

persist_directory = "./chroma_db"

def create_chroma_client():
    client = chromadb.PersistentClient(path=persist_directory)
    return client

def ingest_documents(docs, client=None, collection_name="enterprise_docs"):
    model = get_embedder()
    embeddings = [model.encode(d["text"]) for d in docs]
    if client is None:
        client = create_chroma_client()
    # create collection or get existing
    if collection_name in [c.name for c in client.list_collections()]:
        coll = client.get_collection(collection_name)
    else:
        coll = client.create_collection(collection_name, embedding_function=None)
    ids = [d["id"] for d in docs]
    metadatas = [{"source": d["id"]} for d in docs]
    coll.add(ids=ids, documents=[d["text"] for d in docs], metadatas=metadatas, embeddings=embeddings)
   ## client.persist()
    return coll
