from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict
import json
import os
from dotenv import load_dotenv
from fastapi import HTTPException


class LLMService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in environment variables")
        
        try:
            self.llm = ChatGroq(
                api_key=self.api_key,
                temperature=0.7,
                model_name="mixtral-8x7b-32768"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize LLM: {str(e)}")

    async def analyze_code_structure(self, code: str) -> Dict:
        try:
            messages = [
                SystemMessage(
                    content="You are a code analysis tool that creates flow diagram structures in JSON format."
                ),
                HumanMessage(
                    content=f"""Analyze this code and return only a JSON structure:
                    {code}
                    
                    Response format must be:
                    {{
                        "nodes": [
                            {{"id": number, "label": "string", "type": "string"}}
                        ],
                        "edges": [
                            {{"source": number, "target": number, "label": "string"}}
                        ]
                    }}"""
                )
            ]

            response = await self.llm.ainvoke(messages)

            # Extract JSON from response
            try:
                json_str = response.content
                if not json_str.startswith('{'):
                    start = json_str.find('{')
                    end = json_str.rfind('}') + 1
                    if start != -1 and end != -1:
                        json_str = json_str[start:end]

                result = json.loads(json_str)

                # Validate response structure
                if not isinstance(result, dict) or 'nodes' not in result or 'edges' not in result:
                    raise ValueError("Invalid response structure")

                return result

            except json.JSONDecodeError as e:
                print(f"Raw response: {response.content}")  # For debugging
                raise ValueError(f"Failed to parse JSON response: {str(e)}")

        except Exception as e:
            print(f"Error in analyze_code_structure: {str(e)}")  # For debugging
            raise HTTPException(
                status_code=500,
                detail=f"Code analysis failed: {str(e)}"
            )
