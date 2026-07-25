from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pydantic import BaseModel
from rag import ask_question

from database import create_database

app = FastAPI(
    title="RAGMind AI",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ask-pdf-ai-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "RAGMind AI Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    pdf_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    create_database(pdf_path)

    return {
        "message": "Database Created Successfully"
    }

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        answer = ask_question(request.message)

        return {
            "answer": answer
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.delete("/new-pdf")
def new_pdf():
    return {
        "message": "Ready for new PDF"
    }