import streamlit as st
import os
from typing import Optional, List
from utils.code_formatter import CodeFormatter

class FileHandler:
    def __init__(self):
        self.formatter = CodeFormatter()
        self.allowed_extensions = [".py", ".js", ".java", ".cpp", ".h", ".hpp", ".cs"]

    def render(
        self,
        key: str,
        allowed_types: Optional[List[str]] = None
    ) -> Optional[str]:
        if allowed_types is None:
            allowed_types = [ext[1:] for ext in self.allowed_extensions]

        uploaded_file = st.file_uploader(
            "Upload Code File",
            type=allowed_types,
            key=f"file_upload_{key}",
            help="Drag and drop or click to upload"
        )

        if uploaded_file:
            try:
                content = uploaded_file.read().decode()
                ext = os.path.splitext(uploaded_file.name)[1]
                language = self._get_language_from_extension(ext)
                
                if st.session_state.settings["auto_format_code"]:
                    content = self.formatter.format_code(content, language)
                    
                return content
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                return None
        return None

    def _get_language_from_extension(self, ext: str) -> str:
        extension_map = {
            ".py": "python",
            ".js": "javascript",
            ".java": "java",
            ".cpp": "cpp",
            ".h": "cpp",
            ".hpp": "cpp",
            ".cs": "csharp"
        }
        return extension_map.get(ext, "text")