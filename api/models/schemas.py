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
    description: str
    language: str
    difficulty: str

class LearnRequest(BaseModel):
    main_topic: str
    language: str
    difficulty: str

class FollowUpRequest(BaseModel):
    question: str
    context: Dict[str, Any]
    provider: str = "groq"

class APIResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None