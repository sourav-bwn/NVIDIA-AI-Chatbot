from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os

app = FastAPI(title="NVIDIA NeMo Chat API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_API_URL = os.getenv(
    "NVIDIA_API_URL",
    "https://integrate.api.nvidia.com/v1/chat/completions",
)
MODEL_NAME = os.getenv("MODEL_NAME", "meta/llama-3.3-70b-instruct")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

if not NVIDIA_API_KEY:
    raise ValueError("NVIDIA_API_KEY environment variable is required")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class ChatResponse(BaseModel):
    content: str
    model: str
    finish_reason: str
    usage: dict


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send chat messages to NVIDIA NeMo API and get response"""
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": request.model or MODEL_NAME,
        "messages": [msg.model_dump() for msg in request.messages],
        "max_tokens": request.max_tokens or MAX_TOKENS,
        "temperature": request.temperature or TEMPERATURE,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(NVIDIA_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            return ChatResponse(
                content=data["choices"][0]["message"]["content"],
                model=data["model"],
                finish_reason=data["choices"][0]["finish_reason"],
                usage=data.get("usage", {}),
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"NVIDIA API error: {e.response.text}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}",
            )


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream chat responses from NVIDIA NeMo API"""
    from fastapi.responses import StreamingResponse

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": request.model or MODEL_NAME,
        "messages": [msg.model_dump() for msg in request.messages],
        "max_tokens": request.max_tokens or MAX_TOKENS,
        "temperature": request.temperature or TEMPERATURE,
        "stream": True,
    }

    async def event_generator():
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST", NVIDIA_API_URL, headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data.strip() == "[DONE]":
                            yield "data: [DONE]\n\n"
                            break
                        yield f"data: {data}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": MODEL_NAME}


@app.get("/models")
async def list_models():
    """List available models (example)"""
    return {
        "models": [
            {"id": "meta/llama-3.3-70b-instruct", "name": "Llama 3.3 70B Instruct"},
            {"id": "meta/llama-3.1-8b-instruct", "name": "Llama 3.1 8B Instruct"},
            {"id": "mistralai/mixtral-8x7b-instruct-v0.1", "name": "Mixtral 8x7B"},
            {"id": "google/gemma-7b", "name": "Gemma 7B"},
        ]
    }
