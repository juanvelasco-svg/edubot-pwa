from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional
import logging
import os

from .config import settings
from .chatbot import initialize_edubot, EduBotRAG

logging.basicConfig(
    level=getattr(logging, "INFO", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando EduBot...")
    
    try:
        app.state.edubot = initialize_edubot()
        logger.info("✓ EduBot inicializado")
    except Exception as e:
        logger.error(f"Error inicializando EduBot: {str(e)}")
        app.state.edubot = None
    
    yield
    
    logger.info("Apagando EduBot...")

app = FastAPI(
    title="EduBot API",
    description="API para chatbot educativo RAG",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Demasiadas solicitudes. Por favor, espera un momento."}
    )

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a EduBot API",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "edubot_initialized": app.state.edubot is not None
    }

@app.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(request: Request, chat_request: ChatRequest):
    if not app.state.edubot:
        raise HTTPException(
            status_code=503,
            detail="Servicio no disponible. EduBot no está inicializado."
        )
    
    try:
        response = app.state.edubot.get_response(chat_request.message)
        
        return ChatResponse(
            response=response,
            conversation_id=chat_request.conversation_id
        )
        
    except Exception as e:
        logger.error(f"Error en /chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no manejado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
