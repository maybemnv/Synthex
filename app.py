import streamlit as st
import os
from datetime import datetime
from utils.code_formatter import CodeFormatter
from pages import home, explain, generate, learn

# Page configuration
st.set_page_config(
    page_title="Synthex",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Synthex AI\nAI-powered code explanation and learning platform"
    }
)

# Initialize session state variables if they don't exist
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_code' not in st.session_state:
    st.session_state.current_code = ""
if 'current_explanation' not in st.session_state:
    st.session_state.current_explanation = ""
if 'model_provider' not in st.session_state:
    st.session_state.model_provider = "Groq (Llama 3)"
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "Intermediate"

# Initialize the code formatter
formatter = CodeFormatter()

# Apply custom CSS
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
    /* Code formatting styles */
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
""" + formatter.get_css_styles(), unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">Synthex</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your intelligent coding assistant and tutor</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("Navigation")
    
    # Navigation menu
    page_options = {
        "home": "🏠 Home",
        "explain": "🔍 Code Explanation", 
        "generate": "✨ Code Generation", 
        "learn": "🎓 Interactive Learning"
    }
    
    # Create navigation buttons
    for page_key, page_name in page_options.items():
        if st.button(page_name, key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.experimental_rerun()
    
    st.divider()
    st.header("Settings")
    
    # Language selection
    language = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "Ruby", "Rust", "PHP"],
        index=0
    )
    st.session_state.language = language
    
    # Difficulty level
    difficulty = st.select_slider(
        "Explanation Level",
        options=["Beginner", "Intermediate", "Advanced"],
        value=st.session_state.difficulty
    )
    st.session_state.difficulty = difficulty
    
    # Model selection
    model_provider = st.selectbox(
        "AI Model Provider",
        ["Groq (Llama 3)", "Google AI (Gemini Pro)", "Hugging Face", "OpenAI"],
        index=0
    )
    st.session_state.model_provider = model_provider
    
    st.divider()
    
    # About section
    st.markdown("### About")
    st.markdown("""
    Synthex helps you understand and learn coding concepts through AI-powered explanations and tutorials.
    
    Version: 1.0.0  
    Created: May 2025
    """)

# Main content area - render the selected page
if st.session_state.page == "home":
    home.render()
elif st.session_state.page == "explain":
    explain.render()
elif st.session_state.page == "generate":
    generate.render()
elif st.session_state.page == "learn":
    learn.render()
else:
    # Default to home if unknown page
    home.render()

# Display history in a collapsible section at the bottom
with st.expander("Session History"):
    if not st.session_state.history:
        st.info("Your session history will appear here. Try generating or explaining some code first!")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{item['timestamp']} - {item['mode']} ({item.get('language', '')})"):
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