from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import json
import asyncio
import httpx
from dotenv import load_dotenv

# Add at the top of the file after imports
LLAMA_CONFIG = {
    "model": "llama3-8b-8192",
    "default_temp": 0.7,
    "max_tokens": {
        "explain": 2048,
        "generate": 1024,
        "interactive": 4096
    },
    "context_window": 8192
}

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Synthex API",
    description="Backend API for the Synthex application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models for request/response
class ExplainRequest(BaseModel):
    code: str
    language: str
    difficulty: str = "intermediate"
    focus_areas: List[str] = ["algorithm", "complexity"]
    line_by_line: bool = False
    include_examples: bool = True
    provider: str = "groq"

class GenerateRequest(BaseModel):
    prompt: str
    language: str
    optimization: str = "balanced"
    include_comments: bool = True
    provider: str = "groq"

class LearnRequest(BaseModel):
    topic: str
    subtopic: str
    format: str
    difficulty: str = "intermediate"
    provider: str = "groq"

class FollowUpRequest(BaseModel):
    question: str
    context: Dict[str, Any]
    provider: str = "groq"

class APIResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None

# LLM Provider class
class LLMProvider:
    def __init__(self, provider_name: str = "groq"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in environment variables")
        self.api_base = "https://api.groq.com/openai/v1"
        self.model = "llama3-8b-8192"
        self.client = None

    async def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """Generate a response using Groq's Llama model"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            url = f"{self.api_base}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.9,  # Added for better response quality
                "frequency_penalty": 0.1,  # Reduces repetition
                "presence_penalty": 0.1  # Encourages diverse responses
            }
            
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Groq API error: {str(e)}")

# Helper function to get LLM provider
# Remove provider parameter since we're only using Groq
def get_provider() -> LLMProvider:
    return LLMProvider()

# API endpoints
@app.get("/api/status")
async def get_status():
    """Check API status"""
    return APIResponse(
        success=True,
        data={"status": "online", "version": "1.0.0"}
    )

@app.post("/api/explain", response_model=APIResponse)
async def explain_code(request: ExplainRequest, provider: LLMProvider = Depends(get_provider)):
    """Explain code with AI"""
    try:
        prompt = f"""[INST] As a programming tutor, explain this {request.language} code.
        Difficulty level: {request.difficulty}
        Focus on: {', '.join(request.focus_areas)}
        
        ```{request.language}
        {request.code}
        ```

        Requirements:
        - {'Line-by-line' if request.line_by_line else 'High-level'} explanation
        - {'Include practical examples' if request.include_examples else 'Skip examples'}
        - Use clear markdown formatting
        - Focus on educational value [/INST]"""
        
        explanation = await provider.generate_response(prompt)
        return APIResponse(success=True, data={"explanation": explanation})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate", response_model=APIResponse)
async def generate_code(request: GenerateRequest, provider: LLMProvider = Depends(get_provider)):
    """Generate code with AI"""
    try:
        # Construct prompt for code generation
        prompt = f"""
        You are CodeMentor AI, an educational programming assistant.
        
        TASK: Generate {request.language} code based on the following prompt:
        
        PROMPT: {request.prompt}
        
        REQUIREMENTS:
        - Language: {request.language}
        - Optimization focus: {request.optimization}
        - Include detailed comments: {'Yes' if request.include_comments else 'No'}
        
        The code should be:
        - Well-structured and readable
        - Follow best practices for {request.language}
        - Handle edge cases appropriately
        - Be optimized for {request.optimization}
        
        Return ONLY the code, properly formatted and indented, with appropriate comments.
        """
        
        # Call LLM API
        code = await provider.generate_response(prompt)
        
        # Clean the response to extract just the code
        # This is a simple implementation - you might need more sophisticated parsing
        code = code.strip()
        if "```" in code:
            parts = code.split("```")
            for part in parts:
                if request.language.lower() in part.lower() or len(parts) == 3:
                    # Extract the middle part of ```language\ncode```
                    code = part.strip()
                    # Remove language identifier if present
                    code_lines = code.split("\n")
                    if request.language.lower() in code_lines[0].lower():
                        code = "\n".join(code_lines[1:])
                    break
        
        return APIResponse(
            success=True,
            data={"code": code}
        )
    except Exception as e:
        # Handle any exceptions and return an error response
        return APIResponse(
            success=False,
            error=str(e)
        )

@app.post("/api/interactive", response_model=APIResponse)
async def interactive_learning(request: LearnRequest, provider: LLMProvider = Depends(get_provider)):
    """Generate interactive learning content"""
    try:
        # Construct prompt for learning content
        prompt = f"""
        You are CodeMentor AI, an educational programming tutor.
        
        TASK: Create a {request.format} on {request.topic}/{request.subtopic} at a {request.difficulty} level.
        
        FORMAT: {request.format}
        
        The response should include:
        - Clear explanation of the concept
        - Code examples in a relevant programming language
        - Visual descriptions that could be translated into diagrams
        - Practice problems or exercises (if appropriate)
        - Key points to remember
        
        Format your response using Markdown with clear section headings.
        Make it engaging and educational.
        """
        
        # Call LLM API
        content = await provider.generate_response(prompt, max_tokens=4096)
        
        return APIResponse(
            success=True,
            data={"content": content}
        )
    except Exception as e:
        # Handle any exceptions and return an error response
        return APIResponse(
            success=False,
            error=str(e)
        )