from fastapi import APIRouter, Depends
from api.models.schemas import GenerateRequest, APIResponse
from api.services.llm_provider import LLMProvider, get_provider

router = APIRouter()

@router.post("/generate", response_model=APIResponse)
async def generate_code(request: GenerateRequest, provider: LLMProvider = Depends(get_provider)):
    messages = [
        {"role": "system", "content": "You are an expert programmer who writes clean, efficient code."},
        {"role": "user", "content": f"Generate {request.language} code for:\n{request.prompt}"}
    ]
    try:
        response = await provider.generate_completion(messages)
        return APIResponse(
            success=True,
            data={"generated_code": response["choices"][0]["message"]["content"]},
            error=None
        )
    except Exception as e:
        return APIResponse(success=False, data={}, error=str(e))