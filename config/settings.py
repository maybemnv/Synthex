from pydantic_settings import BaseSettings

LLAMA_CONFIG = {
    "model": "llama-3.1-8b-instant",
    "default_temp": 0.7,
    "max_tokens": {
        "explain": 2048,
        "generate": 1024,
        "interactive": 4096
    },
    "context_window": 8192
}

class Settings(BaseSettings):
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()