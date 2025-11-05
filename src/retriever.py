def retrieve_similar(collection, query_embedding, k=4):
    res = collection.query(query_embeddings=[query_embedding], n_results=k, include=["documents", "metadatas", "distances"])
    # res is a dict with 'documents', 'metadatas'
    return res
