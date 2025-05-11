import streamlit as st
import requests
import json
from datetime import datetime
from utils.code_formatter import CodeFormatter

def render():
    """Render the interactive learning page"""
    
    # Initialize code formatter
    formatter = CodeFormatter()
    
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
        elif main_topic == "Object-Oriented Programming":
            subtopic = st.selectbox(
                "Specific Topic",
                ["Classes & Objects", "Inheritance", "Polymorphism", "Encapsulation", "Abstraction", "Design Principles"]
            )
        elif main_topic == "Web Development":
            subtopic = st.selectbox(
                "Specific Topic",
                ["HTML/CSS Basics", "JavaScript Fundamentals", "API Design", "Authentication", "Frontend Frameworks", "Backend Development"]
            )
        else:
            subtopic = st.selectbox(
                "Specific Topic",
                ["Introduction", "Advanced Concepts", "Best Practices", "Common Patterns"]
            )
    
    # Learning preferences
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox(
            "Programming Language",
            ["Python", "JavaScript", "Java", "C++", "Go"],
            index=0
        )
    
    with col2:
        difficulty = st.select_slider(
            "Learning Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Intermediate"
        )
    
    # Learning format
    learning_format = st.radio(
        "Learning Format",
        ["Concept Explanation", "Interactive Tutorial", "Challenge Problem"],
        horizontal=True
    )
    
    if st.button("Start Learning", type="primary"):
        with st.spinner("Preparing your learning content..."):
            try:
                # Format API request
                # api_url = "http://localhost:8000/api/learn"
                # payload = {
                #     "main_topic": main_topic,
                #     "subtopic": subtopic,
                #     "language": language.lower(),
                #     "difficulty": difficulty.lower(),
                #     "format": learning_format.lower().replace(" ", "_"),
                #     "provider": st.session_state.get("model_provider", "groq").split()[0].lower()
                # }
                #
                # response = requests.post(api_url, json=payload)
                # response.raise_for_status()
                # result = response.json()
                #
                # if result["success"]:
                #     lesson_content = result["data"]["lesson"]
                # else:
                #     st.error(f"API Error: {result['error']}")
                #     return
                
                # For development, generate mock learning content
                if main_topic == "Data Structures" and subtopic == "Linked Lists":
                    lesson_title = "Introduction to Linked Lists"
                    lesson_content = """
                    A linked list is a linear data structure where elements are stored in nodes. 
                    Each node contains data and a reference (link) to the next node in the sequence.
                    
                    #### Key Characteristics:
                    - Dynamic size (can grow or shrink at runtime)
                    - Efficient insertions and deletions
                    - Non-contiguous memory allocation
                    - Sequential access (no random access)
                    """
                    
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
                else:
                    lesson_title = f"{subtopic} in {main_topic}"
                    lesson_content = f"""
                    This is an AI-generated tutorial on {subtopic} in {main_topic} for {language} 
                    at the {difficulty} level, presented as a {learning_format}.
                    
                    ## Overview
                    
                    {subtopic} is an important concept in {main_topic}. Understanding this concept will help you
                    become a better programmer and solve problems more efficiently.
                    
                    ## Key Concepts
                    
                    1. **Fundamental Principles**: The core ideas behind {subtopic}
                    2. **Implementation Details**: How to implement {subtopic} in {language}
                    3. **Common Use Cases**: When and how to apply {subtopic}
                    4. **Performance Considerations**: Understanding the efficiency of {subtopic}
                    
                    ## Best Practices
                    
                    - Always consider edge cases
                    - Follow established naming conventions
                    - Write clean, maintainable code
                    - Test thoroughly
                    """
                    
                    code_example = f"""
                    # Example implementation in {language}
                    # This is a simplified example to demonstrate the concept
                    
                    def example_function(input_data):
                        \"\"\"
                        This function demonstrates {subtopic} in {language}
                        
                        Args:
                            input_data: The data to process
                            
                        Returns:
                            Processed data
                        \"\"\"
                        result = process_data(input_data)
                        return optimize_result(result)
                        
                    def process_data(data):
                        # Processing logic here
                        return transformed_data
                        
                    def optimize_result(data):
                        # Optimization logic here
                        return optimized_data
                    """
                
                # Display the lesson content
                st.markdown(f"## {lesson_title}")
                st.markdown(lesson_content)
                
                # Display code example with syntax highlighting
                st.markdown("### Code Implementation")
                formatted_code = formatter.format_code(code_example, language.lower())
                highlighted_code = formatter.highlight_code(formatted_code, language.lower())
                st.markdown(highlighted_code, unsafe_allow_html=True)
                
                # Interactive elements
                if learning_format == "Interactive Tutorial":
                    st.markdown("### Practice")
                    user_code = st.text_area("Try implementing this yourself:", height=200)
                    
                    if st.button("Check My Code"):
                        st.info("In a full implementation, this would provide feedback on your code.")
                
                elif learning_format == "Challenge Problem":
                    st.markdown("### Challenge")
                    st.markdown(f"""
                    Implement a function that uses {subtopic} to solve the following problem:
                    
                    Given a collection of elements, perform operations efficiently using the principles of {subtopic}.
                    """)
                    
                    challenge_code = st.text_area("Your solution:", height=200)
                    
                    if st.button("Submit Solution"):
                        st.info("In a full implementation, this would evaluate your solution.")
                
                # Understanding check
                st.markdown("### Understanding Check")
                
                q1 = st.radio(
                    f"What is the primary advantage of using {subtopic}?",
                    ["Option A", "Option B", "Option C", "Option D"],
                    index=1
                )
                
                if q1 == "Option B":
                    st.success("Correct! That's the right answer.")
                elif st.button("Check Answer"):
                    st.error("Incorrect. Try again!")
                
                # Next steps
                st.markdown("### Next Steps")
                st.markdown(f"""
                To continue learning about {subtopic}:
                1. Apply these concepts in a real project
                2. Explore advanced techniques 
                3. Practice with more examples
                4. Learn related concepts in {main_topic}
                """)
                
                # Add to history
                if 'history' not in st.session_state:
                    st.session_state.history = []
                    
                st.session_state.history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "mode": "Learning",
                    "language": language,
                    "topic": f"{main_topic} - {subtopic}",
                    "difficulty": difficulty
                })
                
            except Exception as e:
                st.error(f"Error loading learning content: {str(e)}")
    
    # Popular topics section
    with st.expander("Popular Topics"):
        st.markdown("### Most Popular Learning Paths")
        
        popular_topics = [
            ("Data Structures", "Arrays", "Python", "Beginner"),
            ("Algorithms", "Sorting", "JavaScript", "Intermediate"),
            ("Object-Oriented Programming", "Classes & Objects", "Java", "Beginner"),
            ("Web Development", "API Design", "Python", "Intermediate"),
            ("Database Design", "Introduction", "SQL", "Beginner")
        ]
        
        for i, (topic, sub, lang, level) in enumerate(popular_topics):
            if st.button(f"Learn {sub} in {topic} ({lang} - {level})", key=f"popular_{i}"):
                # Set these values in session state and rerun
                st.session_state.learn_main_topic = topic
                st.session_state.learn_subtopic = sub
                st.session_state.learn_language = lang
                st.session_state.learn_difficulty = level
                st.experimental_rerun()