import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    # Add more keys as needed

    # Model configuration
    LLAMA_MODEL: str = "llama3-8b-8192"
    DEFAULT_TEMPERATURE: float = 0.7
    MAX_TOKENS = {
        "explain": 2048,
        "generate": 1024,
        "interactive": 4096
    }
    CONTEXT_WINDOW: int = 8192

    # FastAPI settings
    API_TITLE: str = "CodeMentor AI API"
    API_DESCRIPTION: str = "Backend API for the CodeMentor AI application"
    API_VERSION: str = "1.0.0"

    # CORS settings
    ALLOWED_ORIGINS = ["*"]  # Change for production

settings = Settings()