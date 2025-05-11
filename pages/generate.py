import streamlit as st
import requests
import json
from datetime import datetime
from utils.code_formatter import CodeFormatter

def render():
    """Render the code generation page"""
    
    # Initialize code formatter
    formatter = CodeFormatter()
    
    st.header("Code Generation")
    
    st.markdown("### Describe what you need")
    code_description = st.text_area(
        "Describe the code you want to generate:",
        height=150,
        placeholder="Example: Write a Python function that sorts a list of dictionaries based on a specific key",
        help="Be specific about what the code should do"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox(
            "Target Language",
            ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "Ruby", "Rust", "PHP"],
            index=0 if st.session_state.get("language") == "Python" else ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "Ruby", "Rust", "PHP"].index(st.session_state.get("language", "Python"))
        )
    
    with col2:
        optimization_focus = st.selectbox(
            "Optimization Focus",
            ["Balanced", "Readability", "Performance", "Memory Efficiency", "Brevity"],
            index=0
        )
    
    include_comments = st.checkbox("Include detailed comments", value=True)
    
    if st.button("Generate Code", type="primary"):
        if code_description:
            with st.spinner("Generating code..."):
                try:
                    api_url = "http://localhost:8000/api/generate"
                    payload = {
                        "prompt": code_description,
                        "language": language.lower(),
                        "optimization_focus": optimization_focus.lower(),
                        "include_comments": include_comments,
                        "provider": st.session_state.get("model_provider", "groq").split()[0].lower()
                    }
                    response = requests.post(api_url, json=payload)
                    response.raise_for_status()
                    result = response.json()
                    if result["success"]:
                        generated_code = result["data"]["code"]
                    else:
                        st.error(f"API Error: {result['error']}")
                        return
                except Exception as e:
                    st.error(f"Error generating code: {str(e)}")
                else:
                    formatted_code = formatter.format_code(generated_code, language.lower())
                    highlighted_code = formatter.highlight_code(formatted_code, language.lower())
                    st.markdown("### Generated Code")
                    st.markdown(highlighted_code, unsafe_allow_html=True)
        else:
            st.warning("Please describe what code you want to generate.")
    
    # Tips for better generation results
    with st.expander("Tips for Better Results"):
        st.markdown("""
        ### How to Get Better Code Generation Results
        
        1. **Be specific** about what you want the code to do
        2. **Include input and output examples** when possible
        3. **Specify constraints** like performance requirements
        4. **Mention the context** where the code will be used
        5. **Request specific design patterns** if you have a preference
        """)