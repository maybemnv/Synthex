import streamlit as st

class ThemeToggle:
    def __init__(self):
        if "theme" not in st.session_state:
            st.session_state.theme = "Light"

    def render(self):
        theme = st.sidebar.selectbox(
            "Theme",
            ["Light", "Dark"],
            key="theme_selector",
            on_change=self._handle_theme_change
        )
        self._apply_theme()
        return theme

    def _handle_theme_change(self):
        st.session_state.theme = st.session_state.theme_selector

    def _apply_theme(self):
        if st.session_state.theme == "Dark":
            st.markdown("""
                <style>
                    .stApp {
                        background-color: #1E1E1E;
                        color: #FFFFFF;
                    }
                </style>
            """, unsafe_allow_html=True)