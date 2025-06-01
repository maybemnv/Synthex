from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class ExplainRequest(BaseModel):
    code: str = Field(..., description="Code to explain")
    language: str = Field(..., description="Programming language")
    difficulty: str = Field(default="intermediate", description="Explanation difficulty level")
    focus_areas: List[str] = Field(default=["Logic Flow"], description="Areas to focus on")
    line_by_line: bool = Field(default=False, description="Whether to provide line-by-line explanation")
    include_examples: bool = Field(default=True, description="Whether to include examples")
    provider: str = "groq"

class FileExplainRequest(BaseModel):
    """Request model for file-based code explanation"""
    filename: str = Field(..., description="Original filename")
    detected_language: Optional[str] = Field(None, description="Auto-detected language")
    difficulty: str = Field(default="intermediate", description="Explanation difficulty level")
    focus_areas: List[str] = Field(default=["Logic Flow"], description="Areas to focus on")
    line_by_line: bool = Field(default=False, description="Whether to provide line-by-line explanation")
    include_examples: bool = Field(default=True, description="Whether to include examples")

class GenerateRequest(BaseModel):
    language: str = Field(..., description="Programming language")
    description: str = Field(..., description="Description of code to generate")
    difficulty: str = Field(default="intermediate", description="Code complexity level")
    options: Dict[str, Any] = Field(default_factory=dict, description="Additional generation options")

class FileStats(BaseModel):
    """File statistics model"""
    lines: int = Field(..., description="Number of lines in file")
    characters: int = Field(..., description="Number of characters in file")
    size_kb: float = Field(..., description="File size in KB")
    non_empty_lines: Optional[int] = Field(None, description="Number of non-empty lines")

class ExplanationResponse(BaseModel):
    """Response model for code explanations"""
    explanation: str = Field(..., description="Generated explanation")
    filename: Optional[str] = Field(None, description="Original filename if from file")
    detected_language: Optional[str] = Field(None, description="Detected programming language")
    file_stats: Optional[FileStats] = Field(None, description="File statistics")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")

class CodeGenerationResponse(BaseModel):
    """Response model for code generation"""
    generated_code: str = Field(..., description="Generated code")
    time_complexity: str = Field(..., description="Time complexity analysis")
    space_complexity: str = Field(..., description="Space complexity analysis")
    language: str = Field(..., description="Programming language used")
    description: str = Field(..., description="Original description")

class BatchExplanationResult(BaseModel):
    """Result for individual file in batch processing"""
    filename: str = Field(..., description="Filename")
    success: bool = Field(..., description="Whether processing was successful")
    detected_language: Optional[str] = Field(None, description="Detected language")
    explanation: Optional[str] = Field(None, description="Generated explanation")
    file_stats: Optional[FileStats] = Field(None, description="File statistics")
    error: Optional[str] = Field(None, description="Error message if failed")

class BatchExplanationResponse(BaseModel):
    """Response model for batch file explanation"""
    batch_results: List[BatchExplanationResult] = Field(..., description="Results for each file")
    total_files: int = Field(..., description="Total number of files processed")
    successful: int = Field(..., description="Number of successfully processed files")
    failed: int = Field(..., description="Number of failed files")
    processing_time: Optional[float] = Field(None, description="Total processing time")

class APIResponse(BaseModel):
    """Generic API response wrapper"""
    success: bool = Field(..., description="Whether the request was successful")
    data: Union[
        ExplanationResponse, 
        CodeGenerationResponse, 
        BatchExplanationResponse,
        Dict[str, Any]
    ] = Field(..., description="Response data")
    error: Optional[str] = Field(None, description="Error message if failed")
    timestamp: Optional[str] = Field(None, description="Response timestamp")

class FollowUpRequest(BaseModel):
    """Request model for follow-up questions"""
    question: str = Field(..., description="Follow-up question about the code")
    context: Dict[str, Any] = Field(..., description="Context including original code and explanation")
    provider: Optional[str] = Field(None, description="LLM provider to use")

class FollowUpResponse(BaseModel):
    """Response model for follow-up questions"""
    answer: str = Field(..., description="Answer to the follow-up question")
    context_used: bool = Field(..., description="Whether previous context was used")

class SupportedTypesResponse(BaseModel):
    """Response model for supported file types"""
    supported_extensions: List[str] = Field(..., description="List of supported file extensions")
    max_file_size_kb: int = Field(..., description="Maximum file size in KB")
    max_batch_files: int = Field(..., description="Maximum number of files in batch")
    language_mapping: Dict[str, str] = Field(..., description="Extension to language mapping")

class ValidationResult(BaseModel):
    """File validation result"""
    is_valid: bool = Field(..., description="Whether the file is valid")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    stats: FileStats = Field(..., description="File statistics")

# Configuration models
class ProviderSettings(BaseModel):
    """LLM Provider settings"""
    provider: str = Field(..., description="Provider name")
    model: Optional[str] = Field(None, description="Specific model to use")
    temperature: Optional[float] = Field(0.7, description="Generation temperature")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")

class DownloadOptions(BaseModel):
    """Download configuration options"""
    format: str = Field(default="txt", description="Download format (txt, md, json)")
    include_metadata: bool = Field(default=True, description="Whether to include metadata")
    include_timestamp: bool = Field(default=True, description="Whether to include timestamp")

# Error models
class ValidationError(BaseModel):
    """Validation error details"""
    field: str = Field(..., description="Field that failed validation")
    message: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")

class APIError(BaseModel):
    """API error response"""
    error_type: str = Field(..., description="Type of error")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")

class LearnRequest(BaseModel):
    """Request model for learning mode"""
    main_topic: str = Field(..., description="Main topic to learn about")
    language: str = Field(..., description="Programming language")
    difficulty: str = Field(default="intermediate", description="Learning difficulty level")
    format: str = Field(default="basic", description="Learning format (basic, with_examples, step_by_step, quiz, analogy)")
    sub_topics: Optional[List[str]] = Field(default_factory=list, description="Specific sub-topics to focus on")
    include_exercises: bool = Field(default=True, description="Whether to include practice exercises")
    provider: Optional[str] = Field(None, description="LLM provider to use")
    max_examples: Optional[int] = Field(default=3, description="Maximum number of examples to include")