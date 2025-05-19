from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from api.models.schemas import APIResponse
from api.services.llm_provider import LLMProvider, get_provider

router = APIRouter(
    prefix="/api/visualization",  # Add /api prefix
    tags=["visualization"],
    responses={404: {"description": "Not found"}},
)

class CodeAnalysisRequest(BaseModel):
    code: str

class AlgorithmVisualizationRequest(BaseModel):
    code: str
    input_data: List[Any]

class PerformanceComparisonRequest(BaseModel):
    codes: Dict[str, str]  # {algorithm_name: code}
    input_sizes: List[int]

@router.post("/code-flow", response_model=APIResponse)
async def analyze_code_flow(
    request: CodeAnalysisRequest,
    provider: LLMProvider = Depends(get_provider)
):
    if not request.code:
        return APIResponse(success=False, data={}, error="Code cannot be empty")
    try:
        result = await provider.analyze_code_flow(request.code)
        return APIResponse(success=True, data=result, error=None)
    except Exception as e:
        return APIResponse(success=False, data={}, error=str(e))

@router.post("/algorithm-visualization", response_model=APIResponse)
async def algorithm_visualization(
    request: AlgorithmVisualizationRequest,
    provider: LLMProvider = Depends(get_provider)
):
    try:
        result = await provider.visualize_algorithm_steps(request.code, request.input_data)
        return APIResponse(success=True, data=result, error=None)
    except Exception as e:
        return APIResponse(success=False, data={}, error=str(e))

@router.post("/performance-comparison", response_model=APIResponse)
async def performance_comparison(
    request: PerformanceComparisonRequest,
    provider: LLMProvider = Depends(get_provider)
):
    try:
        result = await provider.compare_algorithm_performance(request.codes, request.input_sizes)
        return APIResponse(success=True, data=result, error=None)
    except Exception as e:
        return APIResponse(success=False, data={}, error=str(e))