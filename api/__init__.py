from fastapi import FastAPI

app = FastAPI(
    title="Synthex API",
    description="AI-powered code explanation, generation, and learning platform",
    version="1.0.0"
)

# Export the app instance
__all__ = ['app']