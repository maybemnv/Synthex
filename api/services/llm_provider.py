import os
import httpx
from fastapi import HTTPException

class LLMProvider:
    def __init__(self, provider_name: str = "groq"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in environment variables")
        self.api_base = "https://api.groq.com/openai/v1"
        self.model = "llama3-8b-8192"

    async def generate_completion(self, messages: list, max_tokens: int = 1000):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base}/chat/completions",
                    headers=headers,
                    json={
                        "model": self.model,
                        "messages": messages,
                        "max_tokens": max_tokens
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM API Error: {str(e)}")

def get_provider():
    return LLMProvider()