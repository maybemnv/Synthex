import streamlit as st
from typing import Dict, List

class LanguageSelector:
    LANGUAGE_INFO = {
        "Python": {
            "extensions": [".py"],
            "icon": "🐍",
            "popularity": 1
        },
        "JavaScript": {
            "extensions": [".js"],
            "icon": "☕",
            "popularity": 2
        },
        "Java": {
            "extensions": [".java"],
            "icon": "☕",
            "popularity": 3
        },
        "C++": {
            "extensions": [".cpp", ".hpp", ".h"],
            "icon": "⚡",
            "popularity": 4
        }
    }

    def __init__(self):
        self.languages = list(self.LANGUAGE_INFO.keys())

    def render(
        self,
        key: str,
        default_index: int = 0,
        show_icons: bool = True,
        on_change: callable = None
    ) -> str:
        display_options = self.languages
        if show_icons:
            display_options = [
                f"{self.LANGUAGE_INFO[lang]['icon']} {lang}"
                for lang in self.languages
            ]

        selected = st.selectbox(
            "Select Language",
            display_options,
            index=default_index,
            key=f"lang_select_{key}",
            on_change=on_change if on_change else None
        )

        # Return clean language name without icon
        return selected.split(" ")[-1] if show_icons else selected

    def get_file_extensions(self, language: str) -> List[str]:
        return self.LANGUAGE_INFO.get(language, {}).get("extensions", [])

    def get_language_from_file(self, filename: str) -> str:
        ext = filename.lower()
        for lang, info in self.LANGUAGE_INFO.items():
            if any(ext.endswith(e) for e in info["extensions"]):
                return lang
        return "Text"