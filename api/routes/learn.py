from fastapi import APIRouter, Depends
from api.models.schemas import GenerateRequest, LearnRequest, APIResponse
from api.services.llm_provider import LLMProvider, get_provider

router = APIRouter()
@router.post("/learn", response_model=APIResponse)
async def learn_code(request: LearnRequest, provider: LLMProvider = Depends(get_provider)):
    messages = [
        {"role": "system", "content": "You are an expert programming tutor."},
        {"role": "user", "content": f"Teach me about {request.topic} ({request.subtopic}) in {request.format} format at {request.difficulty} difficulty."}
    ]
    try:
        response = await provider.generate_completion(messages)
        return APIResponse(
            success=True,
            data={"lesson": response["choices"][0]["message"]["content"]},
            error=None
        )
    except Exception as e:
        return APIResponse(success=False, data={}, error=str(e))