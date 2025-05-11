from fastapi import APIRouter, Depends, Request
from api.models.schemas import LearnRequest, APIResponse
from api.services.llm_provider import LLMProvider, get_provider

router = APIRouter()

# In-memory context store (for demo; use Redis/DB for production)
SESSION_CONTEXT = {}

LEARN_PROMPT_TEMPLATES = {
    "basic": "Teach me about {main_topic} in {language} at a {difficulty} level.",
    "with_examples": "Explain {main_topic} in {language} at a {difficulty} level and provide code examples.",
    "step_by_step": "Give a step-by-step explanation of {main_topic} in {language} for a {difficulty} learner.",
    "quiz": "Teach me about {main_topic} in {language} at a {difficulty} level and then quiz me with 3 questions.",
    "analogy": "Explain {main_topic} in {language} at a {difficulty} level using a real-world analogy."
}

@router.post("/learn", response_model=APIResponse)
async def learn_concept(
    request: LearnRequest,
    fastapi_request: Request,
    provider: LLMProvider = Depends(get_provider),
    template: str = "basic",
    session_id: str = None
):
    # Identify session (use cookie, header, or explicit session_id)
    session_key = session_id or fastapi_request.client.host
    context = SESSION_CONTEXT.get(session_key, [])

    prompt_template = LEARN_PROMPT_TEMPLATES.get(template, LEARN_PROMPT_TEMPLATES["basic"])
    user_prompt = prompt_template.format(
        main_topic=request.main_topic,
        language=request.language,
        difficulty=request.difficulty
    )

    # Add previous context to messages
    messages = [{"role": "system", "content": "You are an expert programming tutor."}]
    messages += context
    messages.append({"role": "user", "content": user_prompt})

    try:
        response = await provider.generate_completion(messages)
        answer = response["choices"][0]["message"]["content"]
        # Update context
        context.append({"role": "user", "content": user_prompt})
        context.append({"role": "assistant", "content": answer})
        SESSION_CONTEXT[session_key] = context[-10:]  # Keep last 10 exchanges

        return APIResponse(
            success=True,
            data={"lesson": answer, "context": context},
            error=None
        )
    except Exception as e:
        return APIResponse(success=False, data={}, error=str(e))