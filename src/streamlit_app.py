import streamlit as st
import requests
import time
import itertools

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="RAGFlow AI Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- SESSION STATE ----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- THEME COLORS ----------
mode_color = "#0f172a" if st.session_state.dark_mode else "#f9fafb"
text_color = "#f9fafb" if st.session_state.dark_mode else "#111827"

# ---------- CUSTOM CSS ----------
st.markdown(f"""
<style>
    .main {{
        background-color: {mode_color};
        color: {text_color};
    }}
    .title-text {{
        font-size: 2.3rem;
        font-weight: 800;
        text-align: center;
        margin-top: 0.2em;
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .stTextInput>div>div>input {{
        border-radius: 10px;
        border: 1px solid #d1d5db;
        padding: 10px;
    }}
    .stButton>button {{
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        color: white;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        transition: 0.3s ease;
    }}
    .stButton>button:hover {{
        background: linear-gradient(90deg, #1e3a8a, #1d4ed8);
        transform: scale(1.02);
    }}
    .response-box {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.5em;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1em;
        color: #111827;
    }}
    footer {{
        text-align: center;
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 2em;
    }}
    .stSidebar .stSuccess, .stSidebar .stError {{
        border-radius: 8px;
        padding: 10px;
        font-weight: 500;
    }}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=100)
st.sidebar.title("RAGFlow AI Platform")
st.sidebar.markdown("🚀 **Enterprise-grade Retrieval-Augmented Generation Demo**")
st.sidebar.divider()
st.sidebar.markdown("""
**Features:**
- 🧠 Query your uploaded documents  
- 📂 Upload new files for live ingestion  
- 🔍 View retrieved context & sources  
- ⚙️ Works with local GPT4All model  
- 💯 100% free & CPU-based
""")
st.sidebar.divider()

# ---------- TOGGLE DARK MODE ----------
if st.sidebar.button("🌓 Toggle Dark/Light Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

# ---------- DOCUMENT INGESTION ----------
st.sidebar.markdown("### 📂 Document Ingestion")
uploaded_files = st.sidebar.file_uploader(
    "Upload documents (PDF, TXT, CSV)", 
    type=["pdf", "txt", "csv"], 
    accept_multiple_files=True
)

if uploaded_files:
    if st.sidebar.button("🚀 Ingest Now"):
        with st.spinner("📚 Uploading & embedding documents..."):
            files_payload = []
            for f in uploaded_files:
                files_payload.append(("files", (f.name, f.getvalue(), f"type/{f.name.split('.')[-1]}")))

            try:
                ingest_resp = requests.post(
                    "http://127.0.0.1:8000/ingest",
                    files=files_payload,
                    timeout=300
                )
                if ingest_resp.status_code == 200:
                    result = ingest_resp.json()
                    st.sidebar.success(f"✅ {result.get('message', 'Documents ingested successfully!')}")
                else:
                    st.sidebar.error(f"❌ Ingestion failed: {ingest_resp.text}")
            except Exception as e:
                st.sidebar.error(f"⚠️ Error during ingestion: {e}")

# ---------- MAIN CONTENT ----------
st.markdown("<div class='title-text'>🧠 Enterprise RAG Assistant</div>", unsafe_allow_html=True)
st.caption("Ask any question based on your uploaded or ingested documents.")

user_question = st.text_input(
    "🔍 Enter your question", 
    placeholder="e.g., What are the key insights from 2023 financial report?"
)

col1, col2 = st.columns([1, 4])
with col1:
    ask_button = st.button("Ask")
with col2:
    clear_button = st.button("🗑️ Clear Chat")

BACKEND_URL = "http://127.0.0.1:8000/query"

def query_backend(question):
    try:
        response = requests.post(BACKEND_URL, json={"question": question}, timeout=600)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"answer": f"⚠️ Backend error: {e}", "sources": []}

# ---------- HANDLE ASK ----------
if ask_button and user_question.strip():
    with st.spinner("🤖 Thinking... please wait."):
        start = time.time()
        data = query_backend(user_question)
        latency = time.time() - start
        st.session_state.history.append({
            "q": user_question,
            "a": data.get("answer", "⚠️ No answer returned."),
            "sources": data.get("sources", []),
            "latency": latency
        })

if clear_button:
    st.session_state.history = []

# ---------- ANIMATED RESPONSE ----------
def animated_text(text, speed=0.02):
    container = st.empty()
    full_text = ""
    for char in itertools.chain(text, "\n"):
        full_text += char
        container.markdown(
            f"<div class='response-box'>🤖 <b>RAGFlow:</b> {full_text}</div>",
            unsafe_allow_html=True
        )
        time.sleep(speed)

# ---------- DISPLAY CHAT ----------
for chat in reversed(st.session_state.history):
    st.markdown(f"**🧑‍💻 You:** {chat['q']}")
    animated_text(chat["a"])
    if chat.get("sources"):
        with st.expander("📚 View Sources"):
            for src in chat["sources"]:
                st.write(f"- {src}")
    st.caption(f"⏱️ Response time: {chat['latency']:.2f}s")
    st.divider()

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("""
<footer>
🔹 Built with <b>Streamlit</b>, <b>FastAPI</b>, and <b>GPT4All</b><br>
© 2025 <b>RAGFlow AI Platform</b> | Crafted by <b>Veneel Kumar A</b> 💻
</footer>
""", unsafe_allow_html=True)
