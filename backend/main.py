from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os
from dotenv import load_dotenv

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

class PromptRequest(BaseModel):
    prompt: str
    system: str = ""

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
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=request.system if request.system else "You are an expert ICT and SMC futures trading mentor specialising in NQ and ES futures.",
        messages=[
            {"role": "user", "content": request.prompt}
        ]
    )
    return {"response": message.content[0].text}