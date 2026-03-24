# import os
# import pandas as pd
# from langchain_community.document_loaders import (
#     PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredHTMLLoader
# )
# from langchain_core.documents import Document
# from ingestion import load_json


# def load_file(file_path, filename):
#     ext = os.path.splitext(filename)[1].lower()
#     if ext == ".pdf":
#         return PyPDFLoader(file_path).load()

#     elif ext == ".txt":
#         return TextLoader(file_path).load()

#     elif ext == ".docx":
#         return Docx2txtLoader(file_path).load()

#     elif ext == ".html":
#         return UnstructuredHTMLLoader(file_path).load()

#     elif ext == ".json":
#         return load_json(file_path)

#     # ⭐ FIXED CSV HANDLING
#     elif ext == ".csv":

#         df = pd.read_csv(file_path)

#         documents = []

#         # ✅ Dataset-level understanding
#         summary = f"""
# This dataset represents an employee directory.

# Columns: {', '.join(df.columns)}

# This dataset contains structured employee information used for HR, reporting, and organizational analysis.
# """

#         documents.append(Document(
#             page_content=summary,
#             metadata={"source": filename, "type": "summary"}
#         ))

#         # ✅ Row-level semantic conversion
#         for _, row in df.iterrows():

#             row_text = ", ".join([
#                 f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])
#             ])

#             documents.append(Document(
#                 page_content=f"Employee record: {row_text}",
#                 metadata={"source": filename, "type": "row"}
#             ))

#         return documents

#     else:
#         raise ValueError(f"Unsupported file type: {ext}")


import os
import pandas as pd
from PIL import Image
import pytesseract

from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredHTMLLoader
)
from langchain_core.documents import Document
from ingestion import load_json


def load_file(file_path, filename):

    ext = os.path.splitext(filename)[1].lower().strip()

    print("📂 Processing file:", filename)
    print("🔍 Detected extension:", ext)

    # -------------------------------
    # 📄 DOCUMENT FILES
    # -------------------------------
    if ext == ".pdf":
        return PyPDFLoader(file_path).load()

    elif ext == ".txt":
        return TextLoader(file_path).load()

    elif ext == ".docx":
        return Docx2txtLoader(file_path).load()

    elif ext == ".html":
        return UnstructuredHTMLLoader(file_path).load()

    elif ext == ".json":
        return load_json(file_path)

    # -------------------------------
    # 📊 CSV FILE
    # -------------------------------
    elif ext == ".csv":

        df = pd.read_csv(file_path)
        documents = []

        summary = f"""
Dataset with columns: {', '.join(df.columns)}
Contains structured data.
"""

        documents.append(Document(
            page_content=summary,
            metadata={"source": filename, "type": "summary"}
        ))

        for _, row in df.iterrows():
            row_text = ", ".join([
                f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])
            ])

            documents.append(Document(
                page_content=f"Record: {row_text}",
                metadata={"source": filename, "type": "row"}
            ))

        return documents

    # -------------------------------
    # 🖼️ IMAGE FILES (PNG, JPG, JPEG)
    # -------------------------------
    elif ext in [".png", ".jpg", ".jpeg"]:

        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)

            if not text.strip():
                text = "No readable text found in image."

        except Exception as e:
            text = f"Image processing failed: {str(e)}"

        return [Document(
            page_content=f"Image Content:\n{text}",
            metadata={"source": filename, "type": "image"}
        )]

    # -------------------------------
    # 🎧 AUDIO FILES (SAFE FALLBACK)
    # -------------------------------
    elif ext in [".mp3", ".wav"]:

        return [Document(
            page_content=f"""
Audio file detected: {filename}

⚠️ Audio transcription is not supported in this deployment.
Please upload transcript or run locally for full support.
""",
            metadata={"source": filename, "type": "audio"}
        )]

    # -------------------------------
    # 🎥 VIDEO FILES (SAFE FALLBACK)
    # -------------------------------
    elif ext in [".mp4", ".avi"]:

        return [Document(
            page_content=f"""
Video file detected: {filename}

⚠️ Video processing is not supported in this environment.
Please upload transcript or extract audio.
""",
            metadata={"source": filename, "type": "video"}
        )]

    # -------------------------------
    # ❌ UNKNOWN FILE TYPE (NO CRASH)
    # -------------------------------
    else:

        return [Document(
            page_content=f"""
Unsupported file type: {ext}

Filename: {filename}

System currently supports:
PDF, DOCX, TXT, CSV, JSON, HTML, PNG, JPG, JPEG, MP3, WAV, MP4, AVI
""",
            metadata={"source": filename, "type": "unknown"}
        )]
