import streamlit as st
import os
from datetime import datetime
from utils.code_formatter import CodeFormatter
from pages import generate, home, explain, learn

# Enhanced components imports
from components.theme_toggle import ThemeToggle
from components.settings_panel import SettingsPanel
from components.advanced_code_editor import AdvancedCodeEditor
from components.language_selector import LanguageSelector
from components.loading import LoadingHandler
from utils.error_handler import ErrorHandler

def init_session_state():
    defaults = {
        "page": "home",
        "history": [],
        "current_code": "",
        "current_explanation": "",
        "model_provider": "Groq (Llama 3)",
        "difficulty": "Intermediate",
        "language": "Python",
        # Enhanced settings
        "theme": "light",
        "settings": {
            "code_theme": "monokai",
            "font_size": "14px",
            "show_line_numbers": True,
            "auto_save": True,
            "dark_mode": False
        }
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def init_components():
    """Initialize enhanced components"""
    components = {
        'theme_toggle': ThemeToggle(),
        'settings_panel': SettingsPanel(),
        'code_editor': AdvancedCodeEditor(),
        'language_selector': LanguageSelector(),
        'loading_handler': LoadingHandler(),
        'error_handler': ErrorHandler()
    }
    return components

def sidebar_navigation():
    st.header("Navigation")
    page_options = {
        "home": "🏠 Home",
        "explain": "🔍 Code Explanation", 
        "generate": "✨ Code Generation", 
        "learn": "🎓 Interactive Learning"
    }
    
    for page_key, page_name in page_options.items():
        if st.button(page_name, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.page = page_key
            st.rerun()
    
    st.divider()
    
    # Enhanced sidebar with components
    components = st.session_state.get('components', {})
    
    # Theme toggle
    if 'theme_toggle' in components:
        st.subheader("🎨 Theme")
        components['theme_toggle'].render()
    
    # Language selector
    if 'language_selector' in components:
        st.subheader("🌐 Language")
        selected_language = components['language_selector'].render(
            key="sidebar_language",
            default_index=0,
            show_icons=True
        )
        st.session_state.language = selected_language
    
    st.divider()
    st.markdown("### About")
    st.markdown("""
    Synthex helps you understand and learn coding concepts through AI-powered explanations and tutorials.

    **Features:**
    • 🔍 Code Explanation
    • ✨ Code Generation  
    • 🎓 Interactive Learning
    • 🎨 Theme Customization
    • 🌐 Multi-language Support

    Version: 2.0.0  
    Created: May 2025
    """)

def render_header(formatter):
    st.markdown("""
    <style>
        /* Modern Color Scheme and Variables */
        :root {
            --primary: #2962ff;
            --primary-light: #768fff;
            --secondary: #304ffe;
            --accent: #00c853;
            --background: #fafafa;
            --text: #212121;
            --text-light: #666666;
            --success: #4caf50;
            --warning: #ff9800;
            --error: #f44336;
        }

        /* Dark mode variables */
        [data-theme="dark"] {
            --background: #121212;
            --text: #ffffff;
            --text-light: #b0b0b0;
        }

        /* Enhanced Header Styling */
        .main-header {
            font-size: 72px;
            font-weight: 900;
            background: linear-gradient(120deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            text-shadow: none;
            padding: 25px 0;
            animation: fadeIn 1s ease-in;
            text-align: center;
        }

        .sub-header {
            font-size: 22px;
            color: var(--text-light);
            margin-top: 0;
            margin-bottom: 50px;
            font-weight: 400;
            letter-spacing: 0.5px;
            animation: slideUp 0.8s ease-out;
            text-align: center;
        }

        /* Enhanced Navigation Buttons */
        .stButton button {
            transition: all 0.3s ease;
            border-radius: 12px;
            border: 2px solid transparent;
            font-weight: 500;
            padding: 12px 24px;
            width: 100%;
            background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%);
        }

        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(41, 98, 255, 0.2);
            border-color: var(--primary-light);
            background: linear-gradient(135deg, var(--primary-light), var(--primary));
            color: white;
        }

        /* Enhanced Code Editor */
        .code-editor {
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid #e0e0e0;
        }

        .code-editor:hover {
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
            border-color: var(--primary-light);
        }

        /* Improved Explanation Container */
        .explanation-container {
            background: linear-gradient(135deg, #f5f9ff 0%, #eef4ff 100%);
            padding: 25px;
            border-radius: 12px;
            border-left: 6px solid var(--primary);
            margin-bottom: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            animation: slideIn 0.5s ease-out;
        }

        /* Enhanced Source Code Display */
        .source {
            background-color: #1e1e1e;
            padding: 1.5em;
            border-radius: 12px;
            margin: 1.2em 0;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.3);
            border: 1px solid #333;
        }

        .source pre {
            margin: 0;
            padding: 0;
            font-family: 'Fira Code', 'Monaco', 'Cascadia Code', monospace;
            font-size: 14px;
            line-height: 1.6;
        }

        /* Enhanced History Cards */
        .history-item {
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid #e8e8e8;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .history-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            transform: scaleY(0);
            transition: transform 0.3s ease;
        }

        .history-item:hover {
            transform: translateX(8px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }

        .history-item:hover::before {
            transform: scaleY(1);
        }

        /* Loading Animation */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        /* Success/Error States */
        .success-message {
            background: linear-gradient(135deg, #e8f5e8 0%, #f0fff0 100%);
            border-left: 6px solid var(--success);
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }

        .error-message {
            background: linear-gradient(135deg, #ffeaea 0%, #fff5f5 100%);
            border-left: 6px solid var(--error);
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideUp {
            from { 
                transform: translateY(30px);
                opacity: 0;
            }
            to { 
                transform: translateY(0);
                opacity: 1;
            }
        }

        @keyframes slideIn {
            from { 
                transform: translateX(-30px);
                opacity: 0;
            }
            to { 
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header { font-size: 48px; padding: 15px 0; }
            .sub-header { font-size: 18px; margin-bottom: 30px; }
            .history-item { padding: 20px; }
            .explanation-container { padding: 20px; }
        }

        /* Enhanced Tooltips */
        .stTooltip {
            font-size: 14px;
            line-height: 1.6;
            padding: 12px 16px;
            border-radius: 8px;
            max-width: 320px;
            background: rgba(0,0,0,0.85);
            backdrop-filter: blur(8px);
        }
        
        /* Empty State Styling */
        .empty-state {
            text-align: center;
            padding: 60px 30px;
            background: linear-gradient(135deg, #f8f9ff 0%, #eef4ff 100%);
            border-radius: 16px;
            margin: 30px 0;
            border: 2px dashed #d0d7ff;
        }
        
        .empty-state-icon {
            font-size: 64px;
            margin-bottom: 20px;
            opacity: 0.8;
        }
        
        .empty-state h3 {
            color: var(--text);
            margin-bottom: 12px;
            font-size: 24px;
        }
        
        .empty-state p {
            color: var(--text-light);
            font-size: 16px;
            line-height: 1.5;
        }
        
        /* Helper Text */
        .helper-text {
            font-size: 14px;
            color: var(--text-light);
            margin-top: 8px;
            font-style: italic;
            line-height: 1.4;
        }

        /* Tab Enhancement */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 12px 20px;
            font-weight: 500;
        }

        /* Settings Panel */
        .settings-section {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #f0f0f0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">Synthex</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your intelligent coding assistant and tutor</div>', unsafe_allow_html=True)

def render_empty_state(section):
    messages = {
        "history": {
            "title": "No History Yet",
            "message": "Your coding journey starts here. Try explaining some code or generating new solutions!",
            "icon": "📝"
        },
        "generation": {
            "title": "Ready to Generate Code",
            "message": "Describe what you want to create, and I'll help you write efficient, clean code.",
            "icon": "✨"
        },
        "explanation": {
            "title": "Ready to Explain Code",
            "message": "Paste your code here, and I'll break it down with detailed explanations.",
            "icon": "🔍"
        },
        "learning": {
            "title": "Ready to Learn",
            "message": "Select a topic to start your personalized learning journey.",
            "icon": "📚"
        }
    }
    
    msg = messages.get(section, {})
    st.markdown(f"""
        <div class="empty-state">
            <div class="empty-state-icon">{msg.get('icon', '✨')}</div>
            <h3>{msg.get('title', 'Getting Started')}</h3>
            <p>{msg.get('message', 'Select an option to begin your coding adventure.')}</p>
        </div>
    """, unsafe_allow_html=True)

def render_history(formatter):
    with st.expander("📚 Session History", expanded=False):
        if not st.session_state.history:
            render_empty_state("history")
        else:
            # Add clear history button
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🗑️ Clear History", type="secondary"):
                    st.session_state.history = []
                    st.rerun()
            
            # Display history items
            for i, item in enumerate(reversed(st.session_state.history)):
                with st.container():
                    st.markdown(f"""
                    <div class="history-item">
                        <h4>🕒 {item['timestamp']} - {item['mode']} ({item.get('language', 'Unknown')})</h4>
                    """, unsafe_allow_html=True)
                    
                    if item['mode'] == "Explanation":
                        if 'full_code' in item:
                            highlighted_code = formatter.highlight_code(
                                item['full_code'], 
                                item['language'].lower()
                            )
                            st.markdown(highlighted_code, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="explanation-container">
                            {item.get('explanation', '')}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    elif item['mode'] == "Generation":
                        st.markdown(f"""
                        <div style='padding: 12px 0; background: #f8f9ff; border-radius: 8px; padding: 16px; margin: 12px 0;'>
                            <strong>🎯 Prompt:</strong> {item.get('prompt', '')}
                        </div>
                        """, unsafe_allow_html=True)
                        if 'code' in item:
                            highlighted_code = formatter.highlight_code(
                                item['code'], 
                                item['language'].lower()
                            )
                            st.markdown(highlighted_code, unsafe_allow_html=True)
                    
                    elif item['mode'] == "Learning":
                        st.markdown(f"""
                        <div style='padding: 12px 0; background: #f0fff0; border-radius: 8px; padding: 16px; margin: 12px 0;'>
                            <strong>📚 Topic:</strong> {item.get('topic', '')}<br>
                            <strong>📊 Difficulty:</strong> {item.get('difficulty', '')}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

def main():
    # Page config
    st.set_page_config(
        page_title="Synthex - AI Coding Assistant",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize everything
    init_session_state()
    
    # Initialize components and store in session state
    if 'components' not in st.session_state:
        try:
            st.session_state.components = init_components()
        except ImportError as e:
            st.warning(f"Some enhanced components are not available: {e}")
            st.session_state.components = {}
    
    formatter = CodeFormatter()
    
    # Render header
    render_header(formatter)
    
    # Sidebar navigation
    with st.sidebar:
        sidebar_navigation()
    
    # Main content area - render the selected page
    page = st.session_state.page
    
    try:
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
    except Exception as e:
        st.error(f"Error loading page: {e}")
        # Fallback to a simple interface
        st.markdown("## Welcome to Synthex")
        st.markdown("Your AI-powered coding assistant is here to help!")
        
        tab1, tab2, tab3 = st.tabs(["🔍 Explain", "✨ Generate", "🎓 Learn"])
        
        with tab1:
            st.markdown("### Code Explanation")
            code_input = st.text_area("Paste your code here:", height=200)
            if st.button("Explain Code"):
                st.info("Code explanation feature will be available here.")
        
        with tab2:
            st.markdown("### Code Generation")
            prompt_input = st.text_area("Describe what you want to create:", height=100)
            if st.button("Generate Code"):
                st.info("Code generation feature will be available here.")
        
        with tab3:
            st.markdown("### Interactive Learning")
            st.selectbox("Choose a topic:", ["Python Basics", "Data Structures", "Algorithms"])
            if st.button("Start Learning"):
                st.info("Learning mode will be available here.")
    
    # Render history
    render_history(formatter)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px 0; color: #666;'>
        Built with ❤️ using Streamlit • 
        <a href='https://github.com/maybemnv/synthex' target='_blank'>GitHub</a> • 
        Version 2.0.0
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()