import streamlit as st

class SettingsPanel:
    def __init__(self):
        if "settings" not in st.session_state:
            st.session_state.settings = {
                "default_language": "Python",
                "code_theme": "monokai",
                "font_size": "14px",
                "show_line_numbers": True,
                "auto_format_code": True,
                "preferred_model": "groq"
            }

    def render(self):
        st.header("Settings")
        
        with st.form("settings_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.selectbox(
                    "Default Language",
                    ["Python", "JavaScript", "Java", "C++"],
                    key="default_language",
                    index=["Python", "JavaScript", "Java", "C++"].index(
                        st.session_state.settings["default_language"]
                    )
                )
                
                st.selectbox(
                    "Code Theme",
                    ["monokai", "github", "dracula", "solarized"],
                    key="code_theme"
                )
                
                st.selectbox(
                    "Font Size",
                    ["12px", "14px", "16px", "18px"],
                    key="font_size"
                )

            with col2:
                st.checkbox(
                    "Show Line Numbers",
                    key="show_line_numbers",
                    value=st.session_state.settings["show_line_numbers"]
                )
                
                st.checkbox(
                    "Auto Format Code",
                    key="auto_format_code",
                    value=st.session_state.settings["auto_format_code"]
                )
                
                st.selectbox(
                    "Preferred AI Model",
                    ["groq", "openai", "anthropic"],
                    key="preferred_model"
                )

            if st.form_submit_button("Save Settings"):
                self._save_settings()
                st.success("Settings saved!")

    def _save_settings(self):
        st.session_state.settings.update({
            "default_language": st.session_state.default_language,
            "code_theme": st.session_state.code_theme,
            "font_size": st.session_state.font_size,
            "show_line_numbers": st.session_state.show_line_numbers,
            "auto_format_code": st.session_state.auto_format_code,
            "preferred_model": st.session_state.preferred_model
        })