# #-🧠-RAG-AI-Platform


Your Local Retrieval-Augmented Generation Assistant for Enterprises

🚀 Overview

Enterprise RAG AI Platform is a local, privacy-friendly, and CPU-efficient system that allows enterprises to query their private documents intelligently using Retrieval-Augmented Generation (RAG).
Built with FastAPI, Streamlit, ChromaDB, and local embedding + LLM models, it provides a complete end-to-end solution for document ingestion, semantic retrieval, and intelligent answering.

🔒 100% local — your documents never leave your system.

🌟 Key Features

✅ Document Ingestion

Upload multiple PDF, TXT, or CSV files

Automatically extract and embed text into a Chroma vector store

✅ Retrieval-Augmented Generation

Fetches most relevant document chunks for each query

Combines them with your question to generate context-aware answers

✅ Interactive UI

Built with Streamlit for real-time chat-style Q&A

Beautiful dark/light themes

Animated AI responses

✅ Modular FastAPI Backend

/ingest → Upload and embed documents

/query → Ask questions and get intelligent answers

✅ Completely Offline

Uses CPU-based local embedding and generation models

No API keys or cloud dependencies

🧩 Project Architecture
rag-ai-platform/
│
├── main.py                 # FastAPI entry point
├        # Streamlit frontend UI
│
├── src/
│   ├── api.py              # Core RAG backend logic (FastAPI app)
│   ├── ingestion.py        # PDF/TXT data loading utilities
│   ├── embed_store.py      # Embedding and Chroma vector store logic
│   ├── retriever.py        # Semantic retrieval from vector DB
│   ├── generator.py       # Local LLM integration
│   |--streamlit.py         # Streamlit frontend UI
├── data/                   # Folder where uploaded docs are stored
├── requirements.txt
└── README.md

⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/veneel77/rag-ai-platform.git
cd rag-ai-platform

2️⃣ Create a virtual environment
python -m venv .venv
.venv\Scripts\activate     # On Windows
# OR
source .venv/bin/activate  # On Linux/Mac

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Start the backend server
uvicorn main:app --reload


Your backend runs at 👉 http://127.0.0.1:8000

5️⃣ Start the Streamlit frontend
streamlit run streamlit_app.py


Your frontend runs at 👉 http://localhost:8502

🧰 Requirements
fastapi
uvicorn
streamlit
chromadb
PyPDF2
pandas
sentence-transformers
langchain
requests

🧱 Future Developments

Here’s what’s planned for future releases of the RAGFlow AI Platform:

🔹 Advanced Document Management

Upload entire folders for batch ingestion

Add document deletion, re-indexing, and update options

Metadata tagging for enterprise datasets (author, department, timestamp)

🔹 Model Enhancements

Integrate local HuggingFace LLMs (e.g., Mistral, Phi-3-mini, Llama 3)

Support hybrid retrieval (BM25 + Vector)

Add fine-tuning support for enterprise domain-specific models

🔹 Improved UI/UX

Persistent chat history

Visual analytics for retrieved chunks

Dynamic theme customization (brand colors, fonts, enterprise mode)

🔹 Enterprise-Grade Features

User authentication and session management

Role-based access control for document visibility

Deployable via Docker, Azure, or AWS ECS

🔹 Integrations

Connect with SharePoint, Confluence, or local drives for ingestion

Integration with email summarization and HR analytics

🚧 Problem Solving & Scalability Plans
Problem	Current Status	Future Solution
Large Document Chunking	Long PDFs exceed context window	Add dynamic chunk splitting & sliding window retrieval
Slow Inference on CPU	GPT4All is CPU-based	Allow GPU/quantized model options
Timeouts on long queries	Fixed timeout (180s)	Stream async responses in real time
Error Handling	Basic HTTP try/except	Centralized FastAPI error handler
Search Relevance	Vector-only retrieval	Combine keyword + semantic hybrid retrieval
Lack of live ingestion	File upload via Streamlit only	Auto-ingestion from watched directory or API call
Scaling for Multi-user	Local session	Plan: Redis-based user sessions + multi-container deployment
🧑‍💻 Developer Info

Project: RAGFlow AI Platform
Developer: 🧠 Veneel Kumar A
Year: 2025
License: MIT
Built With: ❤️ Python, Streamlit, and FastAPI

💬 “Empowering enterprises with local, secure, and intelligent document understanding.”