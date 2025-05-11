"""
Home page for the Synthex application
"""
import streamlit as st
from utils.state_manager import StateManager
from components.code_components import CodeDisplay
from utils.code_formatter import CodeFormatter

def render():
    """Render the home page"""
    formatter = CodeFormatter()
    code_display = CodeDisplay(formatter)
    
    # Main content
    st.markdown("## Welcome to Synthex")
    st.markdown("""
    Your intelligent coding assistant that helps you understand, generate, and learn programming concepts with AI.
    
    ### 🚀 Get Started
    
    Choose a feature from the sidebar or explore the quick-start options below.
    """)
    
    # Feature cards with enhanced design
    st.markdown("""
    <style>
    .feature-card {
        background-color: #f7f9fc;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #4e8cff;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-5px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Explain Code")
        st.markdown("""
        Understand complex code with AI-powered explanations tailored to your level.
        
        - Line-by-line explanations
        - Focus on specific aspects
        - Multiple difficulty levels
        """)
        if st.button("Try Code Explanation", key="try_explain"):
            StateManager.navigate_to("explain")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### ✨ Generate Code")
        st.markdown("""
        Generate code snippets from natural language descriptions.
        
        - Multiple programming languages
        - Optimization focus options
        - Customizable output format
        """)
        if st.button("Try Code Generation", key="try_generate"):
            StateManager.navigate_to("generate")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🎓 Learn Concepts")
        st.markdown("""
        Master programming concepts with interactive tutorials.
        
        - Topic-specific learning paths
        - Interactive exercises
        - Personalized difficulty
        """)
        if st.button("Try Interactive Learning", key="try_learn"):
            StateManager.navigate_to("learn")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity with improved display
    st.markdown("## Recent Activity")
    if 'history' in st.session_state and st.session_state.history:
        # Show last 3 items
        for i, item in enumerate(list(reversed(st.session_state.history))[:3]):
            with st.expander(f"{item['timestamp']} - {item['mode']} ({item.get('language', '')})"):
                if item['mode'] == "Explanation":
                    st.markdown(f"**Language:** {item.get('language', 'Unknown')}")
                    if 'code_snippet' in item:
                        # Just show a snippet in the history view
                        code_snippet = item['code_snippet'][:150] + "..." if len(item.get('code_snippet', '')) > 150 else item.get('code_snippet', '')
                        st.code(code_snippet, language=item.get('language', '').lower())
                    if 'explanation_summary' in item:
                        st.markdown(f"**Summary:** {item.get('explanation_summary', '')}")
                        
                elif item['mode'] == "Generation":
                    st.markdown(f"**Prompt:** {item.get('prompt', '')}")
                    if 'code' in item:
                        st.code(item['code'][:150] + "..." if len(item['code']) > 150 else item['code'], 
                               language=item.get('language', '').lower())
                               
                elif item['mode'] == "Learning":
                    st.markdown(f"**Topic:** {item.get('topic', '')}")
                    st.markdown(f"**Difficulty:** {item.get('difficulty', '')}")
                    
    else:
        st.info("No recent activity. Start by trying one of our features!")
    
    # Tips and tricks with improved UI
    st.markdown("## Tips & Tricks")
    
    tips = {
        "Code Generation": {
            "title": "Better Code Generation Results",
            "content": """
            When generating code, be as specific as possible about what you need.
            
            **Example:** Instead of "Sort a list", try "Sort a list of user objects by their 'last_login' timestamp in descending order".
            
            The more details you provide about inputs, outputs, edge cases, and performance requirements, the better the results will be.
            """
        },
        "Explanation Levels": {
            "title": "Choosing the Right Explanation Level",
            "content": """
            Adjust the explanation level based on your familiarity with the concept:
            
            - **Beginner:** Explains fundamentals and avoids jargon
            - **Intermediate:** Balances depth with clarity
            - **Advanced:** Focuses on optimization and advanced concepts
            
            Don't hesitate to switch levels if an explanation is too basic or too complex.
            """
        },
        "Follow-up Questions": {
            "title": "Using Follow-up Questions Effectively",
            "content": """
            After receiving an explanation, use the follow-up feature to ask about specific aspects you'd like to explore further.
            
            Good follow-up questions:
            - "Why did you use a hash table instead of an array here?"
            - "How would this algorithm's performance change with larger inputs?"
            - "Can you explain how the recursion works in step 3?"
            """
        },
        "Learning Paths": {
            "title": "Creating Effective Learning Plans",
            "content": """
            For the best learning experience:
            
            1. Start with foundational topics before advanced ones
            2. Practice concepts in multiple languages to deepen understanding
            3. Use the interactive tutorial format for hands-on learning
            4. Revisit topics at increasing difficulty levels
            """
        }
    }
    
    selected_tip = st.selectbox(
        "Select a tip:",
        list(tips.keys())
    )
    
    st.markdown(f"### {tips[selected_tip]['title']}")
    st.markdown(tips[selected_tip]['content'])