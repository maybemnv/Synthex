from typing import Dict, List, Any
from langchain_groq import ChatGroq
from pydantic import BaseModel

class LLMAlgorithmAnalyzer:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=st.secrets["GROQ_API_KEY"],
            model_name="mixtral-8x7b-32768"
        )
    
    async def analyze_algorithm(self, code: str, input_data: List[Any]) -> Dict:
        """Use LLM to analyze algorithm and generate visualization steps"""
        
        prompt = f"""
        Analyze this algorithm and generate step-by-step visualization data:
        
        Code:
        {code}
        
        Input Data:
        {input_data}
        
        Generate a JSON response with:
        1. Step-by-step states of the algorithm
        2. Description for each step
        3. Elements being compared/modified in each step
        4. Time complexity analysis
        5. Space complexity analysis
        """
        
        response = await self.llm.achat(prompt)
        visualization_data = self._parse_llm_response(response)
        return visualization_data
    
    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response into visualization format"""
        try:
            # Extract JSON from response
            data = json.loads(response)
            return {
                "initial_state": data["steps"][0]["state"],
                "frames": [
                    {
                        "data": [{
                            "x": list(range(len(step["state"]))),
                            "y": step["state"],
                            "type": "bar",
                            "marker": {
                                "color": self._get_colors(step["highlights"])
                            }
                        }],
                        "layout": {
                            "annotations": [{
                                "text": step["description"],
                                "xref": "paper",
                                "yref": "paper",
                                "x": 0.5,
                                "y": 1.05,
                                "showarrow": False
                            }]
                        }
                    }
                    for step in data["steps"]
                ],
                "complexity": {
                    "time": data["time_complexity"],
                    "space": data["space_complexity"]
                }
            }
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {str(e)}")