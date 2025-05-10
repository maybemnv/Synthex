from pydantic import BaseModel
from typing import List, Optional, Dict, Any

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
    context: str = ""
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