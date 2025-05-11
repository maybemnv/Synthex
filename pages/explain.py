import streamlit as st
import requests
import json
from datetime import datetime
from utils.code_formatter import CodeFormatter

def render():
    """Render the code explanation page"""
    
    # Initialize code formatter
    formatter = CodeFormatter()
    
    st.header("Code Explanation")
    
    # Code input area
    st.markdown("### Enter your code")
    
    # Using Streamlit's code editor
    code = st.text_area(
        "Paste your code here:",
        height=300,
        key="code_input",
        help="Paste the code you want explained",
        value=st.session_state.get("current_code", "")
    )
    
    # Options for explanation
    col1, col2 = st.columns(2)
    with col1:
        focus_areas = st.multiselect(
            "Focus Areas",
            ["Algorithm Steps", "Time Complexity", "Space Complexity", "Best Practices", "Alternative Approaches"],
            default=["Algorithm Steps", "Time Complexity"]
        )
    
    with col2:
        include_examples = st.checkbox("Include examples", value=True)
        show_line_by_line = st.checkbox("Line-by-line explanation", value=False)
    
    # Language and difficulty selection
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox(
            "Language",
            ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "Ruby", "Rust", "PHP"],
            index=0
        )
    
    with col2:
        difficulty = st.select_slider(
            "Explanation Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value=st.session_state.get("difficulty", "Intermediate")
        )
    
    # Explain button
    if st.button("Explain This Code", type="primary"):
        if code:
            with st.spinner("Analyzing your code..."):
                # Format the code before processing
                formatted_code = formatter.format_code(code, language.lower())
                st.session_state.current_code = formatted_code
                
                # Add syntax highlighting for display
                highlighted_code = formatter.highlight_code(formatted_code, language.lower())
                
                # Display formatted code
                st.markdown("### Formatted Code")
                st.markdown(highlighted_code, unsafe_allow_html=True)
                
                try:
                    # Create request to API
                    api_url = "http://localhost:8000/api/explain"
                    
                    # Convert focus areas to the format expected by the API
                    api_focus_areas = [area.lower().replace(" ", "_") for area in focus_areas]
                    
                    payload = {
                        "code": formatted_code,
                        "language": language.lower(),
                        "difficulty": difficulty.lower(),
                        "focus_areas": api_focus_areas,
                        "line_by_line": show_line_by_line,
                        "include_examples": include_examples,
                        "provider": st.session_state.get("model_provider", "groq").split()[0].lower()
                    }
                    
                    # For development purposes, generate a mock explanation
                    # In production, uncomment the API request code
                    
                    # response = requests.post(api_url, json=payload)
                    # if response.status_code == 200:
                    #     result = response.json()
                    #     if result["success"]:
                    #         explanation = result["data"]["explanation"]
                    #     else:
                    #         st.error(f"API Error: {result['error']}")
                    #         return
                    # else:
                    #     st.error(f"API request failed with status code {response.status_code}")
                    #     return
                    
                    # Mock explanation (would come from API)
                    explanation = f"""
                    ## Explanation of {language} Code

                    This code implements a function that performs the following operations:

                    1. **Purpose**: The code is designed to process input data efficiently
                    2. **Algorithm**: Uses a divide-and-conquer approach
                    3. **Time Complexity**: O(n log n) - efficient for large datasets
                    4. **Space Complexity**: O(n) - creates temporary storage proportional to input size

                    ### Key Insights:
                    - The algorithm efficiently handles edge cases
                    - The implementation follows {language} best practices
                    - There's potential for optimization in the inner loop
                    
                    ### Improvement Suggestions:
                    - Consider using built-in functions for better performance
                    - Add error handling for invalid inputs
                    - Improve variable naming for better readability
                    """
                    
                    st.session_state.current_explanation = explanation
                    
                    # Add to history
                    if "history" not in st.session_state:
                        st.session_state.history = []
                        
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "mode": "Explanation",
                        "language": language,
                        "code": code[:100] + "..." if len(code) > 100 else code,
                        "full_code": code,
                        "explanation": explanation
                    })
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter some code to explain.")
    
    # Display explanation if available
    if "current_explanation" in st.session_state and st.session_state.current_explanation:
        st.markdown("### Explanation")
        st.markdown('<div class="explanation-container">', unsafe_allow_html=True)
        st.markdown(st.session_state.current_explanation)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Follow-up options
        st.markdown("### Follow-up")
        follow_up_question = st.text_input("Ask a follow-up question about this code:")
        if st.button("Submit Question"):
            if follow_up_question:
                with st.spinner("Generating answer..."):
                    try:
                        # For development, generate a mock answer
                        # In production, uncomment the API request code
                        
                        # api_url = "http://localhost:8000/api/followup"
                        # payload = {
                        #     "question": follow_up_question,
                        #     "context": {
                        #         "code": st.session_state.current_code,
                        #         "language": language.lower(),
                        #         "previous_explanation": st.session_state.current_explanation
                        #     },
                        #     "provider": st.session_state.get("model_provider", "groq").split()[0].lower()
                        # }
                        # response = requests.post(api_url, json=payload)
                        # response.raise_for_status()
                        # result = response.json()
                        # answer = result["data"]["answer"]
                        
                        # Mock answer
                        answer = f"Answer to: '{follow_up_question}'\n\nThis would be answered by the AI in a real implementation. The answer would be specific to your question and the code you're analyzing."
                        
                        st.info(answer)
                        
                    except Exception as e:
                        st.error(f"Error processing follow-up question: {str(e)}")
            else:
                st.warning("Please enter a follow-up question.")