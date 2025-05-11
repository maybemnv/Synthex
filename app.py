import streamlit as st
import os
from datetime import datetime
from utils.code_formatter import CodeFormatter
from pages import generate, home, explain, learn

def init_session_state():
    defaults = {
        "page": "home",
        "history": [],
        "current_code": "",
        "current_explanation": "",
        "model_provider": "Groq (Llama 3)",
        "difficulty": "Intermediate",
        "language": "Python"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def sidebar_navigation():
    st.header("Navigation")
    page_options = {
        "home": "🏠 Home",
        "explain": "🔍 Code Explanation", 
        "generate": "✨ Code Generation", 
        "learn": "🎓 Interactive Learning"
    }
    for page_key, page_name in page_options.items():
        if st.button(page_name, key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.rerun() 
    st.divider()
    st.markdown("### About")
    st.markdown("""
    Synthex helps you understand and learn coding concepts through AI-powered explanations and tutorials.

    Version: 1.0.0  
    Created: May 2025
    """)

def render_header(formatter):
    st.markdown("""
    <style>
        .main-header {
            font-size: 64px;
            font-weight: 800;
            color: #1e54bb;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            padding: 20px 0;
        }
        .sub-header {
            font-size: 20px;
            color: #555555;
            margin-top: 5px;
            margin-bottom: 40px;
            font-weight: 500;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 16px;
            font-size: 16px;
        }
        .code-editor {
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 15px;
        }
        .explanation-container {
            background-color: #f0f5ff;
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #4e8cff;
            margin-bottom: 20px;
        }
        .source {
            background-color: #272822;
            padding: 1em;
            border-radius: 8px;
            margin: 1em 0;
        }
        .source pre {
            margin: 0;
            padding: 0;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="main-header">Synthex</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your intelligent coding assistant and tutor</p>', unsafe_allow_html=True)

def render_history(formatter):
    with st.expander("Session History"):
        if not st.session_state.history:
            st.info("Your session history will appear here. Try generating or explaining some code first!")
        else:
            for i, item in enumerate(reversed(st.session_state.history)):
                st.markdown(f"**{item['timestamp']} - {item['mode']} ({item.get('language', '')})**")
                if item['mode'] == "Explanation":
                    if 'full_code' in item:
                        highlighted_code = formatter.highlight_code(
                            item['full_code'], 
                            item['language'].lower()
                        )
                        st.markdown(highlighted_code, unsafe_allow_html=True)
                    st.markdown(item.get('explanation', ''))
                elif item['mode'] == "Generation":
                    st.markdown(f"**Prompt**: {item.get('prompt', '')}")
                    if 'code' in item:
                        highlighted_code = formatter.highlight_code(
                            item['code'], 
                            item['language'].lower()
                        )
                        st.markdown(highlighted_code, unsafe_allow_html=True)
                elif item['mode'] == "Learning":
                    st.markdown(f"**Topic**: {item.get('topic', '')}")
                    st.markdown(f"**Difficulty**: {item.get('difficulty', '')}")

def main():
    init_session_state()
    formatter = CodeFormatter()
    render_header(formatter)
    with st.sidebar:
        sidebar_navigation()
    # Main content area - render the selected page
    page = st.session_state.page
    if page == "home":
        home.render()
    elif page == "explain":
        explain.render()
    elif page == "generate":
        generate.render()
    elif page == "learn":
        learn.render()
    else:
        home.render()
    render_history(formatter)

if __name__ == "__main__":
    main()