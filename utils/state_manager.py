"""
Centralized state management for Synthex application.
This module provides a clean interface for managing application state.
"""
import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Optional

class StateManager:
    """
    Manages application state in a centralized way to ensure consistency
    across different pages of the Synthex application.
    """
    
    @staticmethod
    def initialize_state():
        """Initialize all required session state variables if they don't exist"""
        
        # Core navigation and UI state
        if 'page' not in st.session_state:
            st.session_state.page = "home"
        
        # User preferences and settings
        if 'language' not in st.session_state:
            st.session_state.language = "Python"
        if 'model_provider' not in st.session_state:
            st.session_state.model_provider = "Groq (Llama 3)"
        if 'difficulty' not in st.session_state:
            st.session_state.difficulty = "Intermediate"
        
        # Content and history tracking
        if 'history' not in st.session_state:
            st.session_state.history = []
        if 'current_code' not in st.session_state:
            st.session_state.current_code = ""
        if 'current_explanation' not in st.session_state:
            st.session_state.current_explanation = ""
        
        # Learning session tracking
        if "learn_session_id" not in st.session_state:
            st.session_state.learn_session_id = ""
        if "learn_context" not in st.session_state:
            st.session_state.learn_context = []
    
    @staticmethod
    def navigate_to(page: str):
        """Set the current page and trigger a rerun"""
        st.session_state.page = page
        st.rerun()
    
    @staticmethod
    def add_to_history(data: Dict[str, Any]):
        """
        Add a new entry to the history
        
        Args:
            data: Dictionary containing the history entry data
        """
        if 'history' not in st.session_state:
            st.session_state.history = []
        
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
                
        st.session_state.history.append(data)
        
        # Cap history size to prevent memory issues
        if len(st.session_state.history) > 50:
            st.session_state.history = st.session_state.history[-50:]
    
    @staticmethod
    def get_provider_settings():
        """Get the current model provider settings"""
        provider_name = st.session_state.get("model_provider", "Groq (Llama 3)")
        return {
            "provider": provider_name.split()[0].lower(),  # Extract provider name (groq, google, etc.)
            "model": provider_name.split("(")[1].rstrip(")") if "(" in provider_name else None  # Extract model name if available
        }
    
    @staticmethod
    def set_code(code: str):
        """Set the current code"""
        st.session_state.current_code = code
    
    @staticmethod
    def set_explanation(explanation: str):
        """Set the current explanation"""
        st.session_state.current_explanation = explanation
    
    @staticmethod
    def clear_current_content():
        """Clear current code and explanation"""
        st.session_state.current_code = ""
        st.session_state.current_explanation = ""