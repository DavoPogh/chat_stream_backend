from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
import asyncio

app = FastAPI()
llm = ChatOpenAI(streaming=True, temperature=0.7, model_name="gpt-4")

async def generate_response(prompt: str):
    async for chunk in llm.astream(prompt):
        yield f"data: {chunk}\n\n"  # Format SSE

@app.get("/chat")
async def chat_stream(prompt: str):
    return StreamingResponse(generate_response(prompt), media_type="text/event-stream")