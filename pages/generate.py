import streamlit as st
import requests
from datetime import datetime
from typing import Dict, Any
from utils.file_handler import FileHandler
from utils.state_manager import StateManager

def render():
    st.markdown("""
    <div class='header-container'>
        <h1>✨ Code Generation</h1>
        <p class='subtitle'>Transform your ideas into code with AI assistance</p>
    </div>
    """, unsafe_allow_html=True)

    # Two-column layout for main content
    left_col, right_col = st.columns([2, 1])

    with left_col:
        with st.form("code_generation_form", clear_on_submit=False):
            # Language selection with icons
            language_options = {
                "Python": "🐍", "JavaScript": "💛", "Java": "☕",
                "C++": "⚡", "Go": "🔵", "SQL": "📊", 
                "Ruby": "💎", "Rust": "⚙️", "PHP": "🐘"
            }
            
            language = st.selectbox(
                "Select Programming Language",
                options=list(language_options.keys()),
                format_func=lambda x: f"{language_options[x]} {x}",
                key="gen_language"
            )

            # Enhanced description input
            st.markdown("### 📝 Description")
            code_description = st.text_area(
                "Description",
                placeholder="Describe what you want to create...\nExample: Create a function that implements binary search algorithm",
                height=120,
                key="code_description",
                help="Be specific about functionality, inputs, and outputs",
                label_visibility="collapsed"
            )

            # Advanced options in an expander
            with st.expander("⚙️ Advanced Options", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    include_comments = st.toggle(
                        "Include Comments",
                        value=True,
                        key="include_comments"
                    )
                    
                    difficulty = st.select_slider(
                        "Code Complexity",
                        options=["Beginner", "Intermediate", "Advanced"],
                        value="Intermediate",
                        key="gen_difficulty"
                    )

                with col2:
                    optimization_focus = st.radio(
                        "Optimization Priority",
                        ["Balance", "Speed", "Memory", "Readability"],
                        key="optimization_focus",
                        horizontal=False
                    )

            submit = st.form_submit_button(
                "🚀 Generate Code",
                type="primary",
                use_container_width=True
            )

    # Right sidebar with tips and examples
    with right_col:
        st.markdown("### 💡 Tips for Better Results")
        st.info("""
        - Be specific about input/output requirements
        - Mention edge cases to handle
        - Specify any performance constraints
        - Include example usage if possible
        """)
        
        st.markdown("### 📚 Example Prompts")
        with st.expander("View Examples"):
            st.code("Create a function to find the longest palindrome in a string")
            st.code("Implement a stack data structure with push, pop, and peek methods")
            st.code("Write a decorator that caches function results")

    if submit and code_description:
        with st.spinner("🤖 Generating your code..."):
            try:
                # API call setup
                api_url = "http://localhost:8000/api/generate"
                payload = {
                    "language": language.lower(),
                    "description": code_description,
                    "difficulty": difficulty.lower(),
                    "options": {
                        "include_comments": include_comments,
                        "optimization_focus": optimization_focus.lower()
                    }
                }
                
                response = requests.post(
                    api_url, 
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        generated_code = result["data"]["generated_code"]
                        time_complexity = result["data"].get("time_complexity", "O(n)")
                        space_complexity = result["data"].get("space_complexity", "O(1)")
                        
                        # Results section
                        st.markdown("---")
                        st.markdown("### 🎉 Generated Code")
                        
                        # Code display with metrics
                        metrics_col1, metrics_col2 = st.columns(2)
                        with metrics_col1:
                            st.metric("Time Complexity", time_complexity)
                        with metrics_col2:
                            st.metric("Space Complexity", space_complexity)
                        
                        # Code display with syntax highlighting
                        st.code(generated_code, language=language.lower())
                        
                        # Action buttons
                        action_col1, action_col2, action_col3 = st.columns(3)
                        
                        with action_col1:
                            if st.button("📋 Copy to Clipboard"):
                                st.toast("Code copied successfully!", icon="✅")
                        
                        with action_col2:
                            st.download_button(
                                "💾 Save as File",
                                data=generated_code,
                                file_name=f"generated_code{get_file_extension(language)}",
                                mime="text/plain",
                            )
                        
                        with action_col3:
                            st.download_button(
                                "📑 Export Report",
                                data=create_downloadable_content(
                                    generated_code,
                                    time_complexity,
                                    space_complexity,
                                    code_description,
                                    language
                                ),
                                file_name=f"code_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                            )

                        # Add to history
                        StateManager.add_to_history({
                            "mode": "Generation",
                            "language": language,
                            "description": code_description,
                            "code": generated_code,
                            "timestamp": datetime.now().isoformat(),
                            "complexity": {
                                "time": time_complexity,
                                "space": space_complexity
                            }
                        })
                        
                    else:
                        st.error(f"Generation failed: {result.get('error', 'Unknown error')}")
                else:
                    st.error(f"API Error (Status {response.status_code})")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    elif submit:
        st.warning("Please provide a description of what you want to generate.")

# Keep existing utility functions
def get_file_extension(language: str) -> str:
    """Get appropriate file extension for the language"""
    extensions = {
        "python": ".py",
        "javascript": ".js",
        "java": ".java",
        "c++": ".cpp",
        "c": ".c",
        "go": ".go",
        "sql": ".sql",
        "ruby": ".rb",
        "rust": ".rs",
        "php": ".php",
        "html": ".html",
        "css": ".css"
    }
    return extensions.get(language.lower(), ".txt")

def create_downloadable_content(code: str, time_complexity: str, space_complexity: str, 
                              description: str, language: str) -> str:
    """Create formatted content for download"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""/*
Generated Code
Language: {language}
Description: {description}
Generated on: {timestamp}
Time Complexity: {time_complexity}
Space Complexity: {space_complexity}
*/

{code}
"""
    return content