
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "has_key": bool(os.getenv("OPENAI_API_KEY")),
        "model": os.getenv("DEFAULT_MODEL", "belum diset"),
    }