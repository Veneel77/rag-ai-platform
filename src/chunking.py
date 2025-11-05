def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + chunk_size, L)
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0: start = 0
    return chunks
