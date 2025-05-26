import streamlit as st
from streamlit_ace import st_ace

class AdvancedCodeEditor:
    def render(
        self,
        key: str,
        language: str = "python",
        theme: str = "monokai",
        font_size: int = 14,
        show_line_numbers: bool = True,
        initial_value: str = ""
    ):
        code = st_ace(
            value=initial_value,
            language=language.lower(),
            theme=theme,
            font_size=font_size,
            show_line_numbers=show_line_numbers,
            key=f"ace_editor_{key}",
            height=300
        )

        return code

    def with_file_upload(self, key: str):
        uploaded_file = st.file_uploader(
            "Upload code file",
            type=["py", "js", "java", "cpp", "txt"],
            key=f"file_upload_{key}"
        )

        if uploaded_file:
            return uploaded_file.read().decode()
        return None