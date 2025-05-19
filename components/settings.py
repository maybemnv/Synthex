import streamlit as st

class Settings:
    def __init__(self):
        if "settings" not in st.session_state:
            st.session_state.settings = {
                "theme": "dark",
                "animations": True,
                "keyboard_shortcuts": True,
                "code_font_size": 14,
                "syntax_theme": "monokai",
                "show_flow_diagrams": True,
                "show_algo_animation": True,
                "show_perf_charts": True,
                "animation_speed": 1.0,
                "diagram_theme": "default",
            }

    def render(self):
        st.sidebar.markdown("### ⚙️ Settings")
        
        # Theme Toggle
        theme = st.sidebar.select_slider(
            "Theme",
            options=["dark", "light"],
            value=st.session_state.settings["theme"],
            key="theme_toggle"
        )
        
        # Animation Toggle
        animations = st.sidebar.checkbox(
            "Enable Animations",
            value=st.session_state.settings["animations"],
            key="animation_toggle"
        )
        
        # Keyboard Shortcuts
        shortcuts = st.sidebar.checkbox(
            "Enable Keyboard Shortcuts",
            value=st.session_state.settings["keyboard_shortcuts"],
            key="shortcuts_toggle"
        )
        
        # Code Font Size
        font_size = st.sidebar.slider(
            "Code Font Size",
            min_value=12,
            max_value=20,
            value=st.session_state.settings["code_font_size"],
            key="font_size_slider"
        )
        
        # Syntax Theme
        syntax_theme = st.sidebar.selectbox(
            "Syntax Theme",
            options=["monokai", "github-dark", "solarized-dark", "solarized-light"],
            index=0,
            key="syntax_theme_select"
        )
        
        # Visualization Settings
        st.sidebar.markdown("### 📊 Visualization Settings")
        viz_options = st.sidebar.expander("Visualization Options")
        with viz_options:
            st.session_state.settings.update({
                "show_flow_diagrams": st.checkbox("Show Code Flow Diagrams", True),
                "show_algo_animation": st.checkbox("Show Algorithm Animations", True),
                "show_perf_charts": st.checkbox("Show Performance Charts", True),
                "animation_speed": st.slider("Animation Speed", 0.5, 2.0, 1.0),
                "diagram_theme": st.selectbox(
                    "Diagram Theme",
                    ["default", "dark", "forest", "neutral"]
                )
            })
        
        # Update settings
        st.session_state.settings.update({
            "theme": theme,
            "animations": animations,
            "keyboard_shortcuts": shortcuts,
            "code_font_size": font_size,
            "syntax_theme": syntax_theme
        })