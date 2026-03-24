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
import pytesseract
from PIL import Image
import whisper
import ffmpeg

from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredHTMLLoader
)
from langchain_core.documents import Document
from ingestion import load_json


# -------------------------------
# LOAD SPEECH MODEL (once)
# -------------------------------
whisper_model = whisper.load_model("base")


def load_file(file_path, filename):

    ext = os.path.splitext(filename)[1].lower()

    # -------------------------------
    # TEXT FILES
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
    # CSV (Already Good)
    # -------------------------------
    elif ext == ".csv":

        df = pd.read_csv(file_path)
        documents = []

        summary = f"""
Dataset with columns: {', '.join(df.columns)}
Contains structured data for analysis.
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
    # 🖼️ IMAGE → OCR
    # -------------------------------
    elif ext in [".png", ".jpg", ".jpeg"]:

        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

        return [Document(
            page_content=text,
            metadata={"source": filename, "type": "image"}
        )]

    # -------------------------------
    # 🎧 AUDIO → SPEECH TO TEXT
    # -------------------------------
    elif ext in [".mp3", ".wav"]:

        result = whisper_model.transcribe(file_path)
        text = result["text"]

        return [Document(
            page_content=text,
            metadata={"source": filename, "type": "audio"}
        )]

    # -------------------------------
    # 🎥 VIDEO → AUDIO → TEXT
    # -------------------------------
    elif ext in [".mp4", ".avi"]:

        audio_path = file_path + ".wav"

        # Extract audio
        ffmpeg.input(file_path).output(audio_path).run(overwrite_output=True)

        result = whisper_model.transcribe(audio_path)
        text = result["text"]

        return [Document(
            page_content=text,
            metadata={"source": filename, "type": "video"}
        )]

    # -------------------------------
    else:
        raise ValueError(f"Unsupported file type: {ext}")
