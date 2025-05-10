from fastapi import APIRouter, Depends
from api.models.schemas import ExplainRequest, APIResponse
from api.services.llm_provider import LLMProvider, get_provider

router = APIRouter()

@router.post("/explain", response_model=APIResponse)
async def explain_code(request: ExplainRequest, provider: LLMProvider = Depends(get_provider)):
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