from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List
import os
import tempfile
from api.models.schemas import ExplainRequest, APIResponse
from api.services.llm_provider import LLMProvider, get_provider

router = APIRouter()

# Allowed file extensions and size limit
ALLOWED_EXTENSIONS = {'.py', '.js', '.cpp', '.c', '.java', '.html', '.css', '.go', 
                     '.sql', '.rb', '.rs', '.php', '.ts', '.jsx', '.tsx'}
MAX_FILE_SIZE = 500 * 1024  # 500KB

def validate_uploaded_file(file: UploadFile) -> bool:
    """Validate uploaded file"""
    if not file:
        return False
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False
    
    # Check file size (FastAPI doesn't provide size directly, so we'll check during read)
    return True

def detect_language_from_filename(filename: str) -> str:
    """Detect programming language from filename"""
    ext = os.path.splitext(filename)[1].lower()
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.go': 'go',
        '.sql': 'sql',
        '.rb': 'ruby',
        '.rs': 'rust',
        '.php': 'php',
        '.html': 'html',
        '.css': 'css'
    }
    return language_map.get(ext, 'python')

@router.post("/explain", response_model=APIResponse)
async def explain_code(request: ExplainRequest, provider: LLMProvider = Depends(get_provider)):
    """Original explain endpoint for direct code input"""
    messages = [
        {"role": "system", "content": "You are a coding expert who explains code clearly and concisely."},
        {"role": "user", "content": f"""
            Explain this {request.language} code:
            {request.code}
            
            Difficulty level: {request.difficulty}
            Focus areas: {', '.join(request.focus_areas)}
            {'Explain line by line' if request.line_by_line else 'Provide overview'}
            {'Include examples' if request.include_examples else 'No examples needed'}
        """}
    ]
    try:
        response = await provider.generate_completion(messages)
        return APIResponse(
            success=True,
            data={"explanation": response["choices"][0]["message"]["content"]},
            error=None
        )
    except Exception as e:
        return APIResponse(success=False, data={}, error=str(e))

@router.post("/explain/file", response_model=APIResponse)
async def explain_code_from_file(
    file: UploadFile = File(...),
    difficulty: Optional[str] = Form("intermediate"),
    focus_areas: Optional[str] = Form("Logic Flow"),
    line_by_line: Optional[bool] = Form(False),
    include_examples: Optional[bool] = Form(True),
    provider: LLMProvider = Depends(get_provider)
):
    """Enhanced explain endpoint that accepts file uploads"""
    
    # Validate file
    if not validate_uploaded_file(file):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type or file too large. Supported types: " + 
                   ", ".join(ALLOWED_EXTENSIONS)
        )
    
    try:
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE // 1024}KB"
            )
        
        # Decode content
        try:
            code_content = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                code_content = content.decode('latin-1')
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="Could not decode file. Please ensure it's a valid text file."
                )
        
        # Detect language from filename
        detected_language = detect_language_from_filename(file.filename)
        
        # Parse focus areas (comma-separated string to list)
        focus_areas_list = [area.strip() for area in focus_areas.split(",") if area.strip()]
        
        # Create explanation prompt
        messages = [
            {"role": "system", "content": "You are a coding expert who explains code clearly and concisely."},
            {"role": "user", "content": f"""
                Explain this {detected_language} code from file '{file.filename}':
                
                {code_content}
                
                Difficulty level: {difficulty}
                Focus areas: {', '.join(focus_areas_list)}
                {'Explain line by line' if line_by_line else 'Provide overview'}
                {'Include examples' if include_examples else 'No examples needed'}
                
                Please provide a comprehensive explanation that covers the code's purpose, 
                key components, and any notable patterns or techniques used.
            """}
        ]
        
        # Get explanation from LLM
        response = await provider.generate_completion(messages)
        explanation = response["choices"][0]["message"]["content"]
        
        return APIResponse(
            success=True,
            data={
                "explanation": explanation,
                "filename": file.filename,
                "detected_language": detected_language,
                "file_stats": {
                    "lines": len(code_content.split('\n')),
                    "characters": len(code_content),
                    "size_kb": round(len(content) / 1024, 2)
                }
            },
            error=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return APIResponse(
            success=False, 
            data={}, 
            error=f"Error processing file: {str(e)}"
        )

@router.post("/explain/batch", response_model=APIResponse)
async def explain_multiple_files(
    files: List[UploadFile] = File(...),
    difficulty: Optional[str] = Form("intermediate"),
    focus_areas: Optional[str] = Form("Logic Flow"),
    provider: LLMProvider = Depends(get_provider)
):
    """Explain multiple code files at once"""
    
    if len(files) > 5:  # Limit to 5 files max
        raise HTTPException(
            status_code=400,
            detail="Maximum 5 files allowed per batch"
        )
    
    results = []
    
    for file in files:
        try:
            # Validate file
            if not validate_uploaded_file(file):
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": "Invalid file type or size"
                })
                continue
            
            # Read and process file
            content = await file.read()
            
            if len(content) > MAX_FILE_SIZE:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": f"File too large (max {MAX_FILE_SIZE // 1024}KB)"
                })
                continue
            
            # Decode content
            try:
                code_content = content.decode('utf-8')
            except UnicodeDecodeError:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": "Could not decode file"
                })
                continue
            
            # Detect language and get explanation
            detected_language = detect_language_from_filename(file.filename)
            focus_areas_list = [area.strip() for area in focus_areas.split(",")]
            
            # Create concise explanation for batch processing
            messages = [
                {"role": "system", "content": "You are a coding expert. Provide concise but informative code explanations."},
                {"role": "user", "content": f"""
                    Briefly explain this {detected_language} code from '{file.filename}':
                    
                    {code_content[:2000]}{"..." if len(code_content) > 2000 else ""}
                    
                    Focus on: {', '.join(focus_areas_list)}
                    Keep the explanation concise but informative.
                """}
            ]
            
            response = await provider.generate_completion(messages)
            explanation = response["choices"][0]["message"]["content"]
            
            results.append({
                "filename": file.filename,
                "success": True,
                "detected_language": detected_language,
                "explanation": explanation,
                "file_stats": {
                    "lines": len(code_content.split('\n')),
                    "size_kb": round(len(content) / 1024, 2)
                }
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return APIResponse(
        success=True,
        data={
            "batch_results": results,
            "total_files": len(files),
            "successful": len([r for r in results if r["success"]]),
            "failed": len([r for r in results if not r["success"]])
        },
        error=None
    )

@router.get("/explain/supported-types")
async def get_supported_file_types():
    """Get list of supported file types for upload"""
    return JSONResponse({
        "supported_extensions": sorted(list(ALLOWED_EXTENSIONS)),
        "max_file_size_kb": MAX_FILE_SIZE // 1024,
        "max_batch_files": 5
    })