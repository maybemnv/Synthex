import streamlit as st
import requests
import uuid
from datetime import datetime
from utils.code_formatter import CodeFormatter

def render():
    """Render the interactive learning page"""
    
    # Initialize code formatter
    formatter = CodeFormatter()

    # --- Context Tracking ---
    if "learn_session_id" not in st.session_state:
        st.session_state.learn_session_id = str(uuid.uuid4())
    if "learn_context" not in st.session_state:
        st.session_state.learn_context = []

    st.header("Interactive Learning")
    
    # Topic selection
    st.markdown("### Select a Topic to Learn")
    
    col1, col2 = st.columns(2)
    with col1:
        main_topic = st.selectbox(
            "Main Topic",
            ["Data Structures", "Algorithms", "AI", "Object-Oriented Programming", 
             "Functional Programming", "Web Development", "Database Design", 
             "Design Patterns", "Testing"],
            help="Choose a main topic to study.\n" +
                 "Each topic has specific subtopics and learning paths."
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
        elif main_topic == "AI":
            subtopic = st.selectbox(
                "Specific Topic",
                [
                    # Machine Learning
                    "ML - Supervised Learning",
                    "ML - Unsupervised Learning",
                    "ML - Model Evaluation",
                    # Deep Learning
                    "DL - Neural Networks",
                    "DL - CNN Architecture",
                    "DL - RNN & LSTM",
                    # NLP
                    "NLP - Text Processing",
                    "NLP - Word Embeddings",
                    "NLP - Transformers",
                    # Computer Vision
                    "CV - Image Processing",
                    "CV - Object Detection",
                    "CV - Image Segmentation",
                    # Reinforcement Learning
                    "RL - Q-Learning",
                    "RL - Policy Gradients",
                    "RL - Deep RL"
                ]
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
    
    # --- FIX: Always define framework ---
    framework = None
    if main_topic == "AI":
        framework = st.selectbox(
            "Framework",
            [
                "TensorFlow",
                "PyTorch",
                "Scikit-learn",
                "Keras",
                "Hugging Face",
                "OpenCV"
            ],
            help="Select your preferred AI framework:\n" +
                 "• TensorFlow/Keras: Google's ML framework\n" +
                 "• PyTorch: Facebook's ML framework\n" +
                 "• Scikit-learn: For classical ML algorithms\n" +
                 "• Hugging Face: For NLP tasks\n" +
                 "• OpenCV: For computer vision"
        )
    
    # Learning format
    if main_topic == "AI":
        learning_format = st.radio(
            "Learning Format",
            [
                "Concept Explanation",
                "Interactive Tutorial",
                "Challenge Problem",
                "Model Implementation",
                "Dataset Analysis",
                "Model Evaluation"
            ],
            horizontal=True
        )
    else:
        learning_format = st.radio(
            "Learning Format",
            ["Concept Explanation", "Interactive Tutorial", "Challenge Problem"],
            horizontal=True
        )
    
    if st.button("Start Learning", type="primary"):
        with st.spinner("Preparing your learning content..."):
            try:
                api_url = "http://localhost:8000/api/learn"
                payload = {
                    "main_topic": main_topic,
                    "language": language.lower(),
                    "difficulty": difficulty.lower(),
                    "framework": framework.lower() if framework else None,
                    "subtopic": subtopic
                }
                params = {
                    "template": learning_format.lower().replace(" ", "_"),
                    "session_id": st.session_state.learn_session_id
                }
                response = requests.post(api_url, json=payload, params=params)
                response.raise_for_status()
                result = response.json()
                if result["success"]:
                    lesson_content = result["data"]["lesson"]
                    st.session_state.learn_context = result["data"].get("context", [])
                else:
                    st.error(f"API Error: {result['error']}")
                    return
                st.markdown(f"## {main_topic} - {subtopic}")
                st.markdown(lesson_content)
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
            ("AI", "ML - Supervised Learning", "Python", "Beginner"),
            ("AI", "DL - Neural Networks", "Python", "Intermediate"),
            ("AI", "NLP - Transformers", "Python", "Advanced"),
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
                st.rerun()