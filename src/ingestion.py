from pathlib import Path
from typing import List, Dict
from PyPDF2 import PdfReader
import pandas as pd

def load_txt(path: Path) -> str:
    """Load plain text or markdown file"""
    return path.read_text(encoding="utf-8", errors="ignore")

def load_pdf(path: Path) -> str:
    """Extract text from PDF pages safely"""
    text = []
    try:
        reader = PdfReader(str(path))
        for page in reader.pages:
            content = page.extract_text() or ""
            text.append(content)
        return "\n".join(text).strip()
    except Exception as e:
        print(f"[WARN] PDF read failed for {path.name}: {e}")
        return ""

def load_csv(path: Path) -> str:
    """Load CSV as combined text for embedding"""
    try:
        df = pd.read_csv(path)
        return df.to_string(index=False)
    except Exception as e:
        print(f"[WARN] CSV read failed for {path.name}: {e}")
        return ""

def load_documents(data_dir: str) -> List[Dict[str, str]]:
    """Load all supported document types from a folder"""
    p = Path(data_dir)
    docs = []
    for f in p.glob("*"):
        ext = f.suffix.lower()
        if ext in [".txt", ".md"]:
            text = load_txt(f)
        elif ext == ".pdf":
            text = load_pdf(f)
        elif ext == ".csv":
            text = load_csv(f)
        else:
            print(f"[SKIP] Unsupported file type: {f.name}")
            continue

        if text.strip():
            docs.append({"id": str(f), "text": text})
        else:
            print(f"[WARN] Skipped empty file: {f.name}")
    return docs
