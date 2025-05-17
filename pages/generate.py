import streamlit as st
import requests
from datetime import datetime
from typing import Dict, Any

def add_to_history(result: Dict[str, Any], description: str, language: str) -> None:
    """Add generated code to session history"""
    if result["success"]:
        history_item = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "Generation",
            "language": language,
            "prompt": description,
            "code": result["data"]["generated_code"],
            "time_complexity": result["data"].get("time_complexity", "N/A"),
            "space_complexity": result["data"].get("space_complexity", "N/A")
        }
        st.session_state.history.append(history_item)

def render():
    st.markdown("## ✨ Code Generation")
    st.markdown("""
    Let me help you generate code based on your description. 
    I'll write clean, efficient code in your chosen language.
    """)

    with st.form("code_generation_form"):
        language = st.selectbox(
            "Programming Language",
            ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "Ruby", "Rust", "PHP"],
            key="gen_language"
        )
        code_description = st.text_area(
            "What would you like me to create?",
            placeholder="Example: Write a function that sorts a list of numbers in ascending order",
            height=100,
            key="code_description"
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            include_comments = st.checkbox("Include comments", value=True, key="include_comments")
        with col2:
            optimization_focus = st.selectbox(
                "Optimization focus",
                ["Balance", "Speed", "Memory", "Readability"],
                key="optimization_focus"
            )
        with col3:
            difficulty = st.selectbox(
                "Difficulty Level",
                ["Beginner", "Intermediate", "Advanced"],
                index=1,
                key="gen_difficulty"
            )
        submit = st.form_submit_button("Generate Code", type="primary")

    if submit and code_description:
        with st.spinner("Generating code..."):
            try:
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
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                response = requests.post(
                    api_url, 
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                if response.status_code != 200:
                    st.error(f"API Error (Status {response.status_code}): {response.text}")
                    return
                result = response.json()
                if result["success"]:
                    st.markdown("### Generated Code:")
                    st.code(result["data"]["generated_code"], language=language.lower())
                    st.markdown(f"**Time Complexity:** {result['data'].get('time_complexity', 'N/A')}")
                    st.markdown(f"**Space Complexity:** {result['data'].get('space_complexity', 'N/A')}")
                    if st.button("📋 Copy Code"):
                        st.toast("Code copied to clipboard!", icon="📋")
                    add_to_history(result, code_description, language)
                else:
                    st.error(f"Error generating code: {result.get('error', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the API server. Make sure the API server is running.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. The server might be overloaded or down.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
    elif submit:
        st.warning("Please provide a description of the code you want to generate.")