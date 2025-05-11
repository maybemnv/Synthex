import streamlit as st

def render():
    """Render the home page"""
    
    # Main content
    st.markdown("## Welcome to Synthex")
    st.markdown("""
    Your intelligent coding assistant that helps you understand, generate, and learn programming concepts with AI.
    
    ### 🚀 Get Started
    
    Choose a feature from the sidebar or explore the quick-start options below.
    """)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔍 Explain Code")
        st.markdown("Understand complex code with AI-powered explanations.")
        if st.button("Try Code Explanation", key="try_explain"):
            st.session_state.page = "explain"
            st.experimental_rerun()
    
    with col2:
        st.markdown("### ✨ Generate Code")
        st.markdown("Generate code snippets from natural language descriptions.")
        if st.button("Try Code Generation", key="try_generate"):
            st.session_state.page = "generate"
            st.experimental_rerun()
    
    with col3:
        st.markdown("### 🎓 Learn Concepts")
        st.markdown("Master programming concepts with interactive tutorials.")
        if st.button("Try Interactive Learning", key="try_learn"):
            st.session_state.page = "learn"
            st.experimental_rerun()
    
    # Recent activity
    st.markdown("## Recent Activity")
    if 'history' in st.session_state and st.session_state.history:
        # Show last 3 items
        for item in list(reversed(st.session_state.history))[:3]:
            with st.expander(f"{item['timestamp']} - {item['mode']} ({item['language']})"):
                if item['mode'] == "Explanation":
                    st.markdown(f"**Code:** ```{item['code']}```")
                elif item['mode'] == "Generation":
                    st.markdown(f"**Prompt:** {item['prompt']}")
    else:
        st.info("No recent activity. Start by trying one of our features!")
    
    # Tips and tricks
    st.markdown("## Tips & Tricks")
    tip = st.selectbox(
        "Select a tip:",
        [
            "Use specific descriptions for better code generation",
            "Experiment with different explanation levels",
            "Save explanations for future reference",
            "Ask follow-up questions to deepen understanding"
        ]
    )
    
    if "specific descriptions" in tip:
        st.markdown("""
        When generating code, be as specific as possible about what you need.
        
        **Example:** Instead of "Sort a list", try "Sort a list of user objects by their 'last_login' timestamp in descending order".
        """)
    elif "explanation levels" in tip:
        st.markdown("""
        Adjust the explanation level based on your familiarity with the concept.
        
        - **Beginner:** Explains fundamentals and avoids jargon
        - **Intermediate:** Balances depth with clarity
        - **Advanced:** Focuses on optimization and advanced concepts
        """)
    elif "Save explanations" in tip:
        st.markdown("""
        All your explanations are saved in the History tab for easy reference.
        
        You can also copy code snippets directly from the explanation using the "Copy to Clipboard" button.
        """)
    elif "follow-up questions" in tip:
        st.markdown("""
        After receiving an explanation, use the follow-up feature to ask about specific aspects you'd like to explore further.
        
        This helps you gain a deeper understanding of complex concepts.
        """)