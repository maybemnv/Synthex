from fastapi import APIRouter, Depends
from api.models.schemas import GenerateRequest, APIResponse
from api.services.llm_provider import LLMProvider, get_provider

router = APIRouter()

@router.post("/generate", response_model=APIResponse)
async def generate_code(request: GenerateRequest, provider: LLMProvider = Depends(get_provider)):
    # Prompt LLM for code and complexity
    messages = [
        {"role": "system", "content": "You are an expert programmer who writes clean, efficient code and analyzes its complexity."},
        {"role": "user", "content": (
            f"Generate {request.language} code for:\n{request.description}\n\n"
            "After the code, provide:\n"
            "Time Complexity: ...\n"
            "Space Complexity: ...\n"
            "Format your answer as:\n"
            "```<language>\n<code>\n```\n"
            "Time Complexity: <complexity>\n"
            "Space Complexity: <complexity>"
        )}
    ]
    try:
        response = await provider.generate_completion(messages)
        content = response["choices"][0]["message"]["content"]

        # Parse code and complexities from the LLM response
        import re
        code_match = re.search(r"```[\w]*\n(.*?)```", content, re.DOTALL)
        code = code_match.group(1).strip() if code_match else content.strip()
        time_match = re.search(r"Time Complexity:\s*(.*)", content)
        space_match = re.search(r"Space Complexity:\s*(.*)", content)
        time_complexity = time_match.group(1).strip() if time_match else "N/A"
        space_complexity = space_match.group(1).strip() if space_match else "N/A"

        return APIResponse(
            success=True,
            data={
                "generated_code": code,
                "time_complexity": time_complexity,
                "space_complexity": space_complexity
            },
            error=None
        )
    except Exception as e:
        return APIResponse(success=False, data={}, error=str(e))