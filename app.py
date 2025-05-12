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

def render_navigation():
    st.sidebar.selectbox(
        "Mode",
        ["Generate", "Explain", "Learn"],
        help="Choose what you want to do:\n\n" +
             "• Generate: Create new code from descriptions\n" +
             "• Explain: Understand existing code\n" +
             "• Learn: Interactive programming tutorials"
    )

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
        }

        .sub-header {
            font-size: 22px;
            color: var(--text-light);
            margin-top: 0;
            margin-bottom: 50px;
            font-weight: 400;
            letter-spacing: 0.5px;
            animation: slideUp 0.8s ease-out;
        }

        /* Animated Navigation Buttons */
        .stButton button {
            transition: all 0.3s ease;
            border-radius: 8px;
            border: 2px solid transparent;
            font-weight: 500;
        }

        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-color: var(--primary-light);
        }

        /* Enhanced Code Editor */
        .code-editor {
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .code-editor:hover {
            box-shadow: 0 6px 24px rgba(0,0,0,0.15);
        }

        /* Improved Explanation Container */
        .explanation-container {
            background: linear-gradient(135deg, #f5f9ff 0%, #eef4ff 100%);
            padding: 25px;
            border-radius: 12px;
            border-left: 6px solid var(--primary);
            margin-bottom: 25px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
            animation: slideIn 0.5s ease-out;
        }

        /* Enhanced Source Code Display */
        .source {
            background-color: #1e1e1e;
            padding: 1.2em;
            border-radius: 12px;
            margin: 1.2em 0;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.2);
        }

        .source pre {
            margin: 0;
            padding: 0;
            font-family: 'Fira Code', monospace;
        }

        /* History Cards */
        .history-item {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            border: 1px solid #eee;
            transition: all 0.3s ease;
        }

        .history-item:hover {
            transform: translateX(5px);
            border-left: 4px solid var(--primary);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes slideUp {
            from { 
                transform: translateY(20px);
                opacity: 0;
            }
            to { 
                transform: translateY(0);
                opacity: 1;
            }
        }

        @keyframes slideIn {
            from { 
                transform: translateX(-20px);
                opacity: 0;
            }
            to { 
                transform: translateX(0);
                opacity: 1;
            }
        }

        /* Responsive Design Improvements */
        @media (max-width: 768px) {
            .main-header { font-size: 48px; }
            .sub-header { font-size: 18px; }
        }

        /* Enhanced Tooltips */
        .stTooltip {
            font-size: 14px;
            line-height: 1.5;
            padding: 12px 16px;
            border-radius: 8px;
            max-width: 300px;
            background: rgba(0,0,0,0.8);
        }
        
        /* Empty State Styling */
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #f5f9ff 0%, #eef4ff 100%);
            border-radius: 12px;
            margin: 20px 0;
        }
        
        .empty-state-icon {
            font-size: 48px;
            margin-bottom: 16px;
        }
        
        /* Helper Text */
        .helper-text {
            font-size: 14px;
            color: var(--text-light);
            margin-top: 4px;
            font-style: italic;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="main-header">Synthex</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your intelligent coding assistant and tutor</p>', unsafe_allow_html=True)

def render_empty_state(section):
    messages = {
        "history": {
            "title": "No History Yet",
            "message": "Your activity will appear here as you use the application.",
            "icon": "📝"
        },
        "generation": {
            "title": "Ready to Generate Code",
            "message": "Describe what you want to create, and I'll help you write it.",
            "icon": "✨"
        },
        "explanation": {
            "title": "Ready to Explain Code",
            "message": "Paste your code here, and I'll help you understand it.",
            "icon": "🔍"
        },
        "learning": {
            "title": "Ready to Learn",
            "message": "Select a topic to start your learning journey.",
            "icon": "📚"
        }
    }
    
    msg = messages.get(section, {})
    st.markdown(f"""
        <div class="empty-state">
            <div class="empty-state-icon">{msg.get('icon', '✨')}</div>
            <h3>{msg.get('title', 'Getting Started')}</h3>
            <p>{msg.get('message', 'Select an option to begin.')}</p>
        </div>
    """, unsafe_allow_html=True)

def render_history(formatter):
    with st.expander("📚 Session History"):
        if not st.session_state.history:
            st.info("🔍 Your session history will appear here. Try generating or explaining some code first!")
        else:
            for i, item in enumerate(reversed(st.session_state.history)):
                with st.container():
                    st.markdown(f"""
                    <div class="history-item">
                        <h4>🕒 {item['timestamp']} - {item['mode']} ({item.get('language', '')})</h4>
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
                        <div style='padding: 10px 0;'>
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
                        <div style='padding: 10px 0;'>
                            <strong>📚 Topic:</strong> {item.get('topic', '')}<br>
                            <strong>📊 Difficulty:</strong> {item.get('difficulty', '')}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

def main():
    init_session_state()
    formatter = CodeFormatter()
    render_header(formatter)
    with st.sidebar:
        sidebar_navigation()
        render_navigation()
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