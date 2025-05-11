"""
API service layer for Synthex application.
Handles all communication with the backend API.
"""
import streamlit as st
import requests
from typing import Dict, Any, List, Optional

class APIService:
    """
    Service class for handling API calls to the Synthex backend.
    Abstracts API communication details from the UI components.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the API service
        
        Parameters:
            base_url: Base URL of the Synthex API
        """
        self.base_url = base_url
    
    def _handle_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None):
        """
        Generic method to handle API requests
        
        Parameters:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request payload
            params: URL parameters
            
        Returns:
            API response data
        
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            result = response.json()
            
            if not result.get("success", False):
                raise Exception(result.get("error", "Unknown API error"))
                
            return result.get("data", {})
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except ValueError as e:
            raise Exception(f"Invalid API response: {str(e)}")
            
    def explain_code(self, 
                    code: str, 
                    language: str, 
                    difficulty: str, 
                    focus_areas: List[str], 
                    line_by_line: bool, 
                    include_examples: bool,
                    provider: str) -> Dict[str, Any]:
        """
        Request code explanation from the API
        
        Parameters:
            code: Source code to explain
            language: Programming language
            difficulty: Explanation level (beginner, intermediate, advanced)
            focus_areas: Areas to focus on in the explanation
            line_by_line: Whether to explain line by line
            include_examples: Whether to include examples
            provider: AI model provider
            
        Returns:
            Dictionary containing the explanation
        """
        api_focus_areas = [area.lower().replace(" ", "_") for area in focus_areas]
        
        payload = {
            "code": code,
            "language": language.lower(),
            "difficulty": difficulty.lower(),
            "focus_areas": api_focus_areas,
            "line_by_line": line_by_line,
            "include_examples": include_examples,
            "provider": provider
        }
        
        return self._handle_request("POST", "/api/explain", data=payload)
        
    def generate_code(self,
                     prompt: str,
                     language: str,
                     optimization_focus: str,
                     include_comments: bool,
                     provider: str) -> Dict[str, Any]:
        """
        Request code generation from the API
        
        Parameters:
            prompt: Description of the code to generate
            language: Target programming language
            optimization_focus: What to optimize for (readability, performance, etc.)
            include_comments: Whether to include detailed comments
            provider: AI model provider
            
        Returns:
            Dictionary containing the generated code
        """
        payload = {
            "prompt": prompt,
            "language": language.lower(),
            "optimization_focus": optimization_focus.lower(),
            "include_comments": include_comments,
            "provider": provider
        }
        
        return self._handle_request("POST", "/api/generate", data=payload)
        
    def learn_concept(self,
                     main_topic: str,
                     subtopic: str,
                     language: str,
                     difficulty: str,
                     learning_format: str,
                     session_id: str,
                     provider: str) -> Dict[str, Any]:
        """
        Request learning materials from the API
        
        Parameters:
            main_topic: Main topic to learn
            subtopic: Specific subtopic
            language: Programming language
            difficulty: Learning level
            learning_format: Format of the learning materials
            session_id: Session identifier for context tracking
            provider: AI model provider
            
        Returns:
            Dictionary containing the learning materials
        """
        payload = {
            "main_topic": f"{main_topic}: {subtopic}",
            "language": language.lower(),
            "difficulty": difficulty.lower(),
            "provider": provider
        }
        
        params = {
            "template": learning_format.lower().replace(" ", "_"),
            "session_id": session_id
        }
        
        return self._handle_request("POST", "/api/learn", data=payload, params=params)
        
    def check_status(self) -> Dict[str, Any]:
        """
        Check the API status
        
        Returns:
            Dictionary containing the API status
        """
        return self._handle_request("GET", "/api/status")

# Create a singleton instance
api_service = APIService()