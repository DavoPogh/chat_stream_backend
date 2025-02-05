from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autoriser le frontend React (modifie si besoin)
origins = [
    "http://localhost:3000",  # Développement local
    "https://ton-site.com"  # Domaine de production (modifie selon ton cas)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autoriser ces origines
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

llm = ChatOpenAI(streaming=True, temperature=0.7, model_name="gpt-4")

async def generate_response(prompt: str):
    async for chunk in llm.astream(prompt):
        yield f"data: {chunk}\n\n"  # Format SSE

@app.get("/chat")
async def chat_stream(prompt: str):
    return StreamingResponse(generate_response(prompt), media_type="text/event-stream")