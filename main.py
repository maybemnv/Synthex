from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.routes import explain, generate, learn

load_dotenv()

app = FastAPI(
    title="Synthex API",
    description="AI-powered code explanation, generation, and learning platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(explain.router, prefix="/api")
app.include_router(generate.router, prefix="/api")
app.include_router(learn.router, prefix="/api")

@app.get("/api/status")
async def get_status():
    return {
        "success": True,
        "data": {"status": "online", "version": "1.0.0"}
    }