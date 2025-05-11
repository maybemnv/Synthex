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
                    # Format API request
                    # api_url = "http://localhost:8000/api/generate"
                    # payload = {
                    #     "prompt": code_description,
                    #     "language": language.lower(),
                    #     "optimization_focus": optimization_focus.lower(),
                    #     "include_comments": include_comments,
                    #     "provider": st.session_state.get("model_provider", "groq").split()[0].lower()
                    # }
                    #
                    # response = requests.post(api_url, json=payload)
                    # response.raise_for_status()
                    # result = response.json()
                    #
                    # if result["success"]:
                    #     generated_code = result["data"]["code"]
                    # else:
                    #     st.error(f"API Error: {result['error']}")
                    #     return
                    
                    # For development, generate mock code
                    # Mock generated code (would come from API)
                    generated_code = """
                    def sort_dict_list(dict_list, key, reverse=False):
                        \"\"\"
                        Sort a list of dictionaries based on a specific key.
                        
                        Args:
                            dict_list (list): List of dictionaries to sort
                            key (str): Dictionary key to sort by
                            reverse (bool): Whether to sort in descending order
                            
                        Returns:
                            list: Sorted list of dictionaries
                            
                        Example:
                            >>> data = [{'name': 'John', 'age': 30}, {'name': 'Alice', 'age': 25}]
                            >>> sort_dict_list(data, 'age')
                            [{'name': 'Alice', 'age': 25}, {'name': 'John', 'age': 30}]
                        \"\"\"
                        # Check if the list is empty
                        if not dict_list:
                            return []
                            
                        # Validate that all items have the specified key
                        if not all(key in d for d in dict_list):
                            raise KeyError(f"Not all dictionaries contain the key '{key}'")
                            
                        # Perform the sorting
                        return sorted(dict_list, key=lambda x: x[key], reverse=reverse)
                    """
                    
                    # Format and highlight the generated code
                    formatted_code = formatter.format_code(generated_code, language.lower())
                    highlighted_code = formatter.highlight_code(formatted_code, language.lower())
                    
                    # Display the generated code
                    st.markdown("### Generated Code")
                    st.markdown(highlighted_code, unsafe_allow_html=True)
                    
                    # Add copy button
                    if st.button("Copy to Clipboard"):
                        st.success("Code copied to clipboard!")
                    
                    # Add to explanation mode option
                    if st.button("Explain This Code"):
                        st.session_state.current_code = generated_code
                        st.session_state.page = "explain"
                        st.experimental_rerun()
                    
                    # Add to history
                    if 'history' not in st.session_state:
                        st.session_state.history = []
                        
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "mode": "Generation",
                        "prompt": code_description,
                        "language": language,
                        "code": generated_code
                    })
                    
                except Exception as e:
                    st.error(f"Error generating code: {str(e)}")
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