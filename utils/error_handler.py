import streamlit as st
from typing import Optional, Any, Dict
import traceback
import logging

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def handle_error(
        self,
        error: Exception,
        user_message: Optional[str] = None,
        show_traceback: bool = False,
        log_error: bool = True
    ) -> Dict[str, Any]:
        """Handle errors gracefully with optional logging and user feedback"""
        error_type = type(error).__name__
        error_message = str(error)
        
        if log_error:
            self.logger.error(
                f"Error occurred: {error_type} - {error_message}",
                exc_info=True
            )
            
        display_message = user_message or "An error occurred. Please try again."
        
        error_details = {
            "type": error_type,
            "message": error_message,
            "traceback": traceback.format_exc() if show_traceback else None
        }
        
        st.error(display_message)
        
        if show_traceback:
            with st.expander("Error Details"):
                st.code(error_details["traceback"], language="python")
                
        return error_details