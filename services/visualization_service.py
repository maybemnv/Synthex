from typing import Dict, List, Any
from services.llm_service import LLMService  # You need to implement this service

class VisualizationService:
    def __init__(self):
        self.llm_service = LLMService()
        
    async def analyze_code_flow(self, code: str) -> Dict:
        """Generate code flow diagram data using LLM"""
        # Ask the LLM to analyze the code and return a flow graph structure
        graph_data = await self.llm_service.analyze_code_flow(code)
        return graph_data
    
    async def create_algorithm_animation(self, steps: List[Dict]) -> Dict:
        """Create algorithm animation frames using LLM explanations"""
        # Optionally, use LLM to explain each step or generate visualization data
        animation_frames = []
        for step in steps:
            frame = await self.llm_service.explain_algorithm_step(step)
            animation_frames.append(frame)
        return {"frames": animation_frames}
    
    async def analyze_performance(self, 
                                algorithms: Dict[str, callable],
                                input_sizes: List[int]) -> Dict:
        """Analyze algorithm performance (can still use your own analyzer)"""
        # This part may remain unchanged unless you want LLM to predict performance
        results = {}
        for name, func in algorithms.items():
            # Optionally, use LLM to predict or explain performance
            perf = await self.llm_service.estimate_performance(func, input_sizes)
            results[name] = perf
        return results