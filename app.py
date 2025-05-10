import streamlit as st
import requests
import json
import os
from datetime import datetime
from utils.code_formatter import CodeFormatter

# Page configuration
st.set_page_config(
    page_title="Synthex",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Synthex AI\nAI-powered code explanation and learning platform"
    }
)

# Initialize session state variables if they don't exist
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_code' not in st.session_state:
    st.session_state.current_code = ""
if 'current_explanation' not in st.session_state:
    st.session_state.current_explanation = ""

# Initialize the code formatter
formatter = CodeFormatter()

# Apply custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 64px;  /* Increased from 42px */
        font-weight: 800;  /* Made bolder */
        color: #1e54bb;  /* Darker blue for better contrast */
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);  /* Added subtle shadow */
        padding: 20px 0;  /* Added padding */
    }
    .sub-header {
        font-size: 20px;  /* Increased from 18px */
        color: #555555;  /* Darker gray */
        margin-top: 5px;
        margin-bottom: 40px;  /* Increased spacing */
        font-weight: 500;  /* Made slightly bolder */
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        font-size: 16px;
    }
    .code-editor {
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 15px;
    }
    .explanation-container {
        background-color: #f0f5ff;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #4e8cff;
        margin-bottom: 20px;
    }
    /* Code formatting styles */
    .source {
        background-color: #272822;
        padding: 1em;
        border-radius: 8px;
        margin: 1em 0;
    }
    .source pre {
        margin: 0;
        padding: 0;
    }
</style>
""" + formatter.get_css_styles(), unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">Synthex</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your intelligent coding assistant and tutor</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("Settings")
    
    # Mode selection
    mode = st.selectbox(
        "Select Mode",
        ["Code Explanation", "Code Generation", "Interactive Learning"],
        index=0
    )
    
    # Language selection
    language = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "Ruby", "Rust", "PHP"],
        index=0
    )
    
    # Difficulty level
    difficulty = st.select_slider(
        "Explanation Level",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Intermediate"
    )
    
    # Model selection
    model_provider = st.selectbox(
        "AI Model Provider",
        ["Groq (Llama 3)", "Google AI (Gemini Pro)", "Hugging Face", "OpenAI"],
        index=0
    )
    
    st.divider()
    
    # About section
    st.markdown("### About")
    st.markdown("""
    CodeMentor AI helps you understand and learn coding concepts through AI-powered explanations and tutorials.
    
    Version: 1.0.0  
    Created: May 2025
    """)

# Main content area with tabs for different features
tabs = st.tabs(["🔍 Explain", "✨ Generate", "🎓 Learn", "📚 History"])

# Explain tab
with tabs[0]:
    if mode == "Code Explanation":
        st.header("Code Explanation")
        
        # Code input area
        st.markdown("### Enter your code")
        
        # Using Streamlit's code editor (native since recent versions)
        code = st.text_area(
            "Paste your code here:",
            height=300,
            key="code_input",
            help="Paste the code you want explained",
            value=st.session_state.current_code
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
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "mode": "Explanation",
                        "language": language,
                        "code": code[:100] + "..." if len(code) > 100 else code,
                        "full_code": code,
                        "explanation": explanation
                    })
            else:
                st.warning("Please enter some code to explain.")
        
        # Display explanation if available
        if st.session_state.current_explanation:
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
                        # Mock answer (would come from API)
                        st.info(f"Answer to: '{follow_up_question}'\n\nThis would be answered by the AI in a real implementation. The answer would be specific to your question and the code you're analyzing.")

# Generate tab
with tabs[1]:
    if mode == "Code Generation":
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
            gen_language = st.selectbox(
                "Target Language",
                ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "Ruby", "Rust", "PHP"],
                index=0 if language == "Python" else ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "Ruby", "Rust", "PHP"].index(language)
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
                    formatted_code = formatter.format_code(generated_code, gen_language.lower())
                    highlighted_code = formatter.highlight_code(formatted_code, gen_language.lower())
                    
                    # Display the generated code
                    st.markdown("### Generated Code")
                    st.markdown(highlighted_code, unsafe_allow_html=True)
                    
                    # Add copy button
                    if st.button("Copy to Clipboard"):
                        st.success("Code copied to clipboard!")
                    
                    # Add to explanation mode option
                    if st.button("Explain This Code"):
                        st.session_state.current_code = generated_code
                        st.session_state.mode = "Code Explanation"
                        st.experimental_rerun()
                    
                    # Add to history
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "mode": "Generation",
                        "prompt": code_description,
                        "language": gen_language,
                        "code": generated_code
                    })
            else:
                st.warning("Please describe what code you want to generate.")

# Learn tab
with tabs[2]:
    if mode == "Interactive Learning":
        st.header("Interactive Learning")
        
        # Topic selection
        st.markdown("### Select a Topic to Learn")
        
        col1, col2 = st.columns(2)
        with col1:
            main_topic = st.selectbox(
                "Main Topic",
                ["Data Structures", "Algorithms", "Object-Oriented Programming", "Functional Programming", 
                 "Web Development", "Database Design", "Design Patterns", "Testing"]
            )
        
        with col2:
            if main_topic == "Data Structures":
                subtopic = st.selectbox(
                    "Specific Topic",
                    ["Arrays", "Linked Lists", "Stacks & Queues", "Trees", "Graphs", "Hash Tables", "Heaps"]
                )
            elif main_topic == "Algorithms":
                subtopic = st.selectbox(
                    "Specific Topic",
                    ["Sorting", "Searching", "Dynamic Programming", "Greedy Algorithms", "Recursion", "Graph Algorithms"]
                )
            else:
                subtopic = st.selectbox(
                    "Specific Topic",
                    ["Introduction", "Advanced Concepts", "Best Practices", "Common Patterns"]
                )
        
        # Learning format
        learning_format = st.radio(
            "Learning Format",
            ["Concept Explanation", "Interactive Tutorial", "Challenge Problem"],
            horizontal=True
        )
        
        if st.button("Start Learning", type="primary"):
            with st.spinner("Preparing your learning content..."):
                # Mock learning content (would come from API)
                st.markdown("### Introduction to Linked Lists")
                
                st.markdown("""
                A linked list is a linear data structure where elements are stored in nodes. 
                Each node contains data and a reference (link) to the next node in the sequence.
                
                #### Key Characteristics:
                - Dynamic size (can grow or shrink at runtime)
                - Efficient insertions and deletions
                - Non-contiguous memory allocation
                - Sequential access (no random access)
                """)
                
                st.markdown("### Basic Implementation")
                
                code_example = """
                class Node:
                    def __init__(self, data):
                        self.data = data
                        self.next = None
                
                class LinkedList:
                    def __init__(self):
                        self.head = None
                    
                    def append(self, data):
                        new_node = Node(data)
                        
                        # If the list is empty
                        if self.head is None:
                            self.head = new_node
                            return
                            
                        # Traverse to the end of the list
                        last = self.head
                        while last.next:
                            last = last.next
                            
                        # Append the new node
                        last.next = new_node
                        
                    def print_list(self):
                        current = self.head
                        while current:
                            print(current.data, end=" -> ")
                            current = current.next
                        print("None")
                """
                
                st.code(code_example, language="python")
                
                # Interactive elements
                st.markdown("### Understanding Check")
                
                q1 = st.radio(
                    "What is the time complexity of appending to a linked list?",
                    ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                    index=2
                )
                
                if q1 == "O(n)":
                    st.success("Correct! Appending requires traversing to the end of the list, which is O(n).")
                
                # Add visualization
                st.markdown("### Visual Representation")
                st.image("https://via.placeholder.com/800x200?text=Linked+List+Visualization", 
                         caption="Linked List Structure")
                
                # Next steps
                st.markdown("### Next Steps")
                st.markdown("""
                To continue learning about linked lists:
                1. Try implementing the code above
                2. Add methods for insertion and deletion
                3. Explore doubly linked lists
                4. Try solving linked list problems
                """)

# History tab
with tabs[3]:
    st.header("Session History")
    
    if not st.session_state.history:
        st.info("Your session history will appear here. Try generating or explaining some code first!")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{item['timestamp']} - {item['mode']} ({item['language']})"):
                if item['mode'] == "Explanation":
                    highlighted_code = formatter.highlight_code(
                        item['full_code'], 
                        item['language'].lower()
                    )
                    st.markdown(highlighted_code, unsafe_allow_html=True)
                    st.markdown(item['explanation'])
                elif item['mode'] == "Generation":
                    st.markdown(f"**Prompt**: {item['prompt']}")
                    highlighted_code = formatter.highlight_code(
                        item['code'], 
                        item['language'].lower()
                    )
                    st.markdown(highlighted_code, unsafe_allow_html=True)