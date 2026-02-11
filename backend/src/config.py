from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    groq_api_key: str
    model_name: str = "llama-3.1-8b-instant"
    max_tokens: int = 800
    temperature: float = 0.3
    chunk_size: int = 800
    chunk_overlap: int = 150
    top_k: int = 4
    documents_path: str = "documentos"
    vectorstore_path: str = "vectorstore"
    rate_limit_per_minute: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

os.makedirs(settings.documents_path, exist_ok=True)
os.makedirs(settings.vectorstore_path, exist_ok=True)
