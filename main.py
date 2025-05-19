from fastapi import FastAPI
from api.routes import explain, generate, learn, visualization

app = FastAPI(title="Synthex API")

# Register all routes
app.include_router(explain.router)
app.include_router(generate.router)
app.include_router(learn.router)
app.include_router(visualization.router)

@app.get("/api/status")
async def status():
    return {"success": True, "message": "API is running"}