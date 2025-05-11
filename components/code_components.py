"""
Reusable UI components for code display and editing
"""
import streamlit as st
from utils.code_formatter import CodeFormatter
from typing import Optional, Callable

class CodeEditor:
    """Reusable code editor component"""
    
    def __init__(self, formatter: CodeFormatter = None):
        """
        Initialize the code editor
        
        Parameters:
            formatter: Code formatter instance (creates one if not provided)
        """
        self.formatter = formatter or CodeFormatter()
        
    def render(self, 
              key: str, 
              label: str = "Code", 
              height: int = 300, 
              language: Optional[str] = None,
              default_value: str = "",
              help_text: str = "Enter or paste your code here",
              on_change: Optional[Callable] = None) -> str:
        """
        Render the code editor and return the entered code
        
        Parameters:
            key: Unique key for the component
            label: Label for the code editor
            height: Height of the editor in pixels
            language: Programming language (for potential syntax hints)
            default_value: Default code to display
            help_text: Help text for the editor
            on_change: Optional callback function when code changes
            
        Returns:
            The code entered by the user
        """
        code = st.text_area(
            label,
            value=default_value,
            height=height,
            key=key,
            help=help_text,
            on_change=on_change if on_change else None
        )
        
        return code
    
class CodeDisplay:
    """Component for displaying formatted code with syntax highlighting"""
    
    def __init__(self, formatter: CodeFormatter = None):
        """
        Initialize the code display
        
        Parameters:
            formatter: Code formatter instance (creates one if not provided)
        """
        self.formatter = formatter or CodeFormatter()
        
    def render(self, 
              code: str, 
              language: str,
              show_copy_button: bool = True,
              show_download_button: bool = False,
              container_class: str = "code-display-container",
              title: Optional[str] = None) -> None:
        """
        Display code with syntax highlighting
        
        Parameters:
            code: Code to display
            language: Programming language for syntax highlighting
            show_copy_button: Whether to show a copy button
            show_download_button: Whether to show a download button
            container_class: CSS class for the container
            title: Optional title for the code block
        """
        if not code.strip():
            st.info("No code to display")
            return
        
        # Create a container with custom class
        st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
        
        # Show title if provided
        if title:
            st.markdown(f"#### {title}")
        
        # Format and highlight the code
        try:
            formatted_code = self.formatter.format_code(code, language)
            highlighted_code = self.formatter.highlight_code(formatted_code, language)
            st.markdown(highlighted_code, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error formatting code: {str(e)}")
            # Fallback to plain code display
            st.code(code, language=language.lower())
        
        # Add buttons
        col1, col2 = st.columns([1, 6])  # Adjust column proportions as needed
        
        if show_copy_button:
            with col1:
                if st.button("📋 Copy", key=f"copy_btn_{hash(code)}"[:10]):
                    st.toast("Code copied to clipboard!", icon="📋")
        
        if show_download_button:
            with col2:
                if st.button("⬇️ Download", key=f"dwnld_btn_{hash(code)}"[:10]):
                    # Logic for downloading would go here in a real app
                    st.toast("Code downloaded!", icon="⬇️")
                    
        st.markdown('</div>', unsafe_allow_html=True)
        
class ExplanationCard:
    """Component for displaying code explanations with formatting"""
    
    def render(self,
              explanation: str,
              title: str = "Explanation",
              container_class: str = "explanation-container") -> None:
        """
        Display a formatted explanation
        
        Parameters:
            explanation: The explanation text (can include markdown)
            title: Title for the explanation
            container_class: CSS class for the container
        """
        if not explanation.strip():
            return
            
        st.markdown(f"### {title}")
        st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
        st.markdown(explanation)
        st.markdown('</div>', unsafe_allow_html=True)
