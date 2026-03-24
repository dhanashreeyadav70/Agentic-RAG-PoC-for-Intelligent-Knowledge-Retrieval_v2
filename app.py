import streamlit as st
import tempfile

from file_loader import load_file
from chunker import split_documents
from vector_store import create_vector_store
from retrieval import HybridRetriever
from workflow import build_graph

st.set_page_config(page_title="AI Assistant", layout="wide")

st.title("🧠 Agentic RAG PoC for Intelligent Knowledge Retrieval")

# -------------------------------
# SESSION STATE
# -------------------------------
if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload file (text, image, audio, video)",
    type=["pdf","docx","txt","csv","json","html","png","jpg","jpeg","mp3","wav","mp4","avi"]
)

# if uploaded_file:

#     with tempfile.NamedTemporaryFile(delete=False) as tmp:
#         tmp.write(uploaded_file.read())
#         file_path = tmp.name

#     docs = load_file(file_path, uploaded_file.name)
#     docs = split_documents(docs)

#     vector_db = create_vector_store(docs, uploaded_file.name)
#     retriever = HybridRetriever(docs, vector_db)

#     # ✅ overwrite retriever (single active KB)
#     st.session_state.retriever = retriever

#     st.success(f"{uploaded_file.name} loaded successfully")

# -------------------------------
# CHAT INPUT
# -------------------------------
query = st.chat_input("Ask anything...")

if query:

    if st.session_state.retriever is None:
        st.warning("⚠️ Please upload a file first")
    else:

        # Display user message
        st.chat_message("user").write(query)

        result = st.session_state.graph.invoke({
            "query": query,
            "retriever": st.session_state.retriever
        })

        answer = result.get("answer", "No response")

        # Display assistant response
        st.chat_message("assistant").write(answer)

        # Store chat history
        st.session_state.chat_history.append({
            "user": query,
            "assistant": answer
        })

import streamlit as st
import os
from file_loader import load_file

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="Multi-Modal RAG Loader", layout="wide")

st.title("📂 Multi-Modal File Upload & Processing")

uploaded_file = st.file_uploader(
    "Upload any file",
    type=[
        "pdf","docx","txt","csv","json","html","htm",
        "png","jpg","jpeg",
        "mp3","wav",
        "mp4","avi","mpeg4"
    ]
)

if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully ✅")

    try:
        with st.spinner("Processing file..."):
            docs = load_file(file_path, uploaded_file.name)

        st.subheader("📄 Extracted Content")
        st.write(docs[0]["page_content"][:3000])

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------
for chat in st.session_state.chat_history:
    st.chat_message("user").write(chat["user"])
    st.chat_message("assistant").write(chat["assistant"])
