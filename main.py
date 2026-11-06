from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = FastAPI()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")  # Jika menggunakan Ollama, ini akan mengarah ke localhost
)

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    try:
        response = client.chat.completions.create(
            model=os.getenv("DEFAULT_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "Anda adalah asisten yang membantu."},
                {"role": "user", "content": req.question}
            ]
        )
        return AskResponse(answer=response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))