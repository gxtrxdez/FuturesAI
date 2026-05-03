from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class Message(BaseModel):
    role: str
    content: str

class PromptRequest(BaseModel):
    prompt: str
    system: str = ""
    history: Optional[List[Message]] = []

@app.get("/")
def read_root():
    return {"message": "FuturesAI backend is running"}

@app.post("/ask-ai")
def ask_ai(request: PromptRequest):
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": request.prompt}
        ]
    )
    return {"response": message.content[0].text}

@app.post("/ask-concept")
def ask_concept(request: PromptRequest):
    if request.history and len(request.history) > 0:
        messages = [{"role": m.role, "content": m.content} for m in request.history]
    else:
        messages = [{"role": "user", "content": request.prompt}]

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=request.system if request.system else "You are an expert ICT and SMC futures trading mentor specialising in NQ and ES futures.",
        messages=messages
    )
    return {"response": message.content[0].text}