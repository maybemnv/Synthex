from fastapi import FastAPI
from dotenv import load_dotenv
import os

def setup_api():
    """Setup function for the API"""
    # Load environment variables
    load_dotenv()
    
    # Verify API key
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY not found in .env file")
    
    # Initialize FastAPI app
    app = FastAPI(
        title="CodeMentor AI API",
        description="Llama-powered programming assistant",
        version="1.0.0"
    )
    
    return app