import os
import httpx
import json
import re
from typing import Dict, List, Any
from langchain_core.messages import SystemMessage, HumanMessage
from fastapi import HTTPException

class LLMProvider:
    def __init__(self, provider_name: str = "groq"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in environment variables")
        self.api_base = "https://api.groq.com/openai/v1"
        self.model = "llama3-8b-8192"

    def _extract_json(self, text):
        """
        Extract the first JSON object from a string.
        """
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            return match.group(1)
        return text  # fallback

    async def analyze_code_flow(self, code: str) -> Dict:
        messages = [
            SystemMessage(content="You are a code analysis tool that creates flow diagram structures in JSON format."),
            HumanMessage(content=f"""Analyze this code and return only a JSON structure.
Respond ONLY with valid JSON. Do not include any explanation or markdown.
{code}
Response format must be:
{{
    "nodes": [{{"id": number, "label": "string", "type": "string"}}],
    "edges": [{{"source": number, "target": number, "label": "string"}}]
}}""")
        ]
        response = await self.generate_completion(messages)
        response_json = self._extract_json(response)
        try:
            return json.loads(response_json)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Invalid LLM response: {str(e)}\nRaw: {response}")

    async def visualize_algorithm_steps(self, code: str, input_data: List[Any]) -> Dict:
        messages = [
            SystemMessage(content="You are an algorithm visualization tool. Output step-by-step JSON for animation."),
            HumanMessage(content=f"""Analyze this algorithm and generate step-by-step visualization data.
Respond ONLY with valid JSON. Do not include any explanation or markdown.
Code:
{code}
Input Data:
{input_data}
Response format:
{{
    "steps": [
        {{"step": int, "description": "string", "state": dict, "highlight": list}}
    ],
    "complexity": {{"time": "string", "space": "string"}}
}}""")
        ]
        response = await self.generate_completion(messages)
        response_json = self._extract_json(response)
        try:
            return json.loads(response_json)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Invalid LLM response: {str(e)}\nRaw: {response}")

    async def compare_algorithm_performance(self, codes: Dict[str, str], input_sizes: List[int]) -> Dict:
        messages = [
            SystemMessage(content="You are a performance analysis tool. Compare algorithms and output JSON chart data."),
            HumanMessage(content=f"""Compare the following algorithms for time and space complexity.
Respond ONLY with valid JSON. Do not include any explanation or markdown.
Algorithms:
{codes}
Input Sizes:
{input_sizes}
Response format:
{{
    "algorithms": [
        {{"name": "string", "time": [float], "space": [float]}}
    ]
}}""")
        ]
        response = await self.generate_completion(messages)
        response_json = self._extract_json(response)
        try:
            return json.loads(response_json)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Invalid LLM response: {str(e)}\nRaw: {response}")

    def _serialize_messages(self, messages):
        # Converts LangChain messages to OpenAI-style dicts
        result = []
        for msg in messages:
            if hasattr(msg, "content"):
                if msg.__class__.__name__ == "SystemMessage":
                    result.append({"role": "system", "content": msg.content})
                elif msg.__class__.__name__ == "HumanMessage":
                    result.append({"role": "user", "content": msg.content})
                else:
                    result.append({"role": "assistant", "content": msg.content})
            else:
                # fallback: treat as string
                result.append({"role": "user", "content": str(msg)})
        return result

    async def generate_completion(self, messages: list, max_tokens: int = 1000):
        payload = {
            "model": self.model,
            "messages": self._serialize_messages(messages),
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}/chat/completions",
                json=payload,
                headers=headers,
                timeout=60
            )
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"LLM API Error: {response.text}")
            return response.json()["choices"][0]["message"]["content"]
    

def get_provider():
    return LLMProvider()