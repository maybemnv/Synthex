"""
Code explanation page for the Synthex application
"""
import streamlit as st
from datetime import datetime
from utils.state_manager import StateManager
from utils.api_service import api_service
from utils.code_formatter import CodeFormatter
from components.code_components import CodeEditor, CodeDisplay, ExplanationCard

def handle_explanation_request(code, language, difficulty, focus_areas, show_line_by_line, include_examples):
    """Handle the code explanation request"""
    
    if not code.strip():
        st.warning("Please enter code to explain.")
        return
        
    with st.spinner("Generating explanation..."):
        try:
            # Get provider settings from state
            provider_settings = StateManager.get_provider_settings()
            
            # Call API service
            result = api_service.explain_code(
                code=code,
                language=language,
                difficulty=difficulty,
                focus_areas=focus_areas,
                line_by_line=show_line_by_line,
                include_examples=include_examples,
                provider=provider_settings["provider"]
            )
            
            # Extract explanation
            explanation = result.get("explanation", "")
            
            # Update state
            StateManager.set_code(code)
            StateManager.set_explanation(explanation)
            
            # Create a summary (first 150 chars)
            explanation_summary = explanation[:150] + "..." if len(explanation) > 150 else explanation
            code_snippet = code[:150] + "..." if len(code) > 150 else code
            
            # Add to history
            StateManager.add_to_history("Explanation", {
                "language": language,
                "full_code": code,
                "code_snippet": code_snippet,
                "explanation": explanation,
                "explanation_summary": explanation_summary,
                "difficulty": difficulty,
                "focus_areas": focus_areas
            })
            
            return explanation
            
        except Exception as e:
            st.error(f"Error generating explanation: {str(e)}")
            return None

def render():
    """Render the code explanation page"""
    
    # Initialize components
    formatter = CodeFormatter()
    code_editor = CodeEditor(formatter)
    code_display = CodeDisplay(formatter)
    explanation_card = ExplanationCard()
    
    st.header("Code Explanation")
    
    # Code input area
    st.markdown("### Enter your code")
    
    code = code_editor.render(
        key="code_input",
        label="Paste your code here:",
        height=300,
        default_value=st.session_state.get("current_code", ""),
        help_text="Paste the code you want explained"
    )
    
    # Options for explanation in two columns
    col1, col2 = st.columns(2)
    
    # Left column - Focus areas
    with col1:
        focus_areas = st.multiselect(
            "Focus Areas",
            ["Logic Flow", "Time Complexity", "Space Complexity", "Best Practices", "Edge Cases"],
            default=["Logic Flow"],
            help="Select what aspects to focus on in the explanation"
        )
    
    # Right column - Options
    with col2:
        include_examples = st.checkbox("Include examples", value=True)
        show_line_by_line = st.checkbox("Line-by-line explanation", value=False)
    
    # Language and difficulty selection
    col1, col2 = st.columns(2)
    
    # Language selection - left column
    with col1:
        language = st.selectbox(
            "Language",
            ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "Ruby", "Rust", "PHP"],
            index=0 if st.session_state.get("language") == "Python" else 
                  ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "Ruby", "Rust", "PHP"].index(st.session_state.get("language", "Python"))
        )
    
    # Difficulty selection - right column
    with col2:
        explanation_level = st.select_slider(
            "Explanation Detail Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Intermediate",
            help="Choose explanation complexity:\n" +
                 "• Beginner: Basic concepts, step-by-step\n" +
                 "• Intermediate: More technical details\n" +
                 "• Advanced: In-depth analysis & optimizations"
        )
    
    # Explain button
    if st.button("Explain Code", type="primary"):
        explanation = handle_explanation_request(
            code, language, explanation_level, focus_areas, 
            show_line_by_line, include_examples
        )
    
    # Display explanation if available
    if "current_explanation" in st.session_state and st.session_state.current_explanation:
        explanation_card.render(
            explanation=st.session_state.current_explanation,
            title="Explanation",
            container_class="explanation-container"
        )
        
        # Follow-up options
        st.markdown("### Ask a Follow-up Question")
        follow_up_question = st.text_input(
            "Have a specific question about this code?",
            placeholder="Example: What's the time complexity of this algorithm?"
        )
        
        if st.button("Submit Question", key="submit_followup"):
            if follow_up_question:
                with st.spinner("Generating answer..."):
                    try:
                        # Get provider settings
                        provider_settings = StateManager.get_provider_settings()
                        
                        # Prepare payload
                        payload = {
                            "question": follow_up_question,
                            "context": {
                                "code": st.session_state.current_code,
                                "language": language.lower(),
                                "previous_explanation": st.session_state.current_explanation
                            },
                            "provider": provider_settings["provider"]
                        }
                        
                        # In a real implementation, we would call the API service here
                        # This is a placeholder since the API endpoint wasn't in the provided code
                        st.info("This feature would call the follow-up API endpoint in a complete implementation.")
                        
                    except Exception as e:
                        st.error(f"Error processing follow-up question: {str(e)}")
            else:
                st.warning("Please enter a follow-up question.")
                
    # Tips for better explanations
    with st.expander("Tips for Better Explanations"):
        st.markdown("""
        ### How to Get Better Code Explanations
        
        1. **Provide complete code** rather than fragments when possible
        2. **Choose focus areas** that are most relevant to your needs
        3. **Adjust difficulty level** based on your familiarity with the concepts
        4. **Use line-by-line mode** for detailed understanding of complex algorithms
        5. **Ask follow-up questions** to dive deeper into specific aspects
        """)