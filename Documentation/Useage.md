# Synthex User Guide

## Getting Started

1. **Launch the app:**  
   - Start backend: `uvicorn main:app --reload --port 8000`
   - Start frontend: `streamlit run app.py`
2. **Navigate using the sidebar:**  
   - Select "Generate", "Explain", or "Learn" mode.

## Features

### Code Generation
- Select **Code Generation**.
- Enter a prompt (e.g., "Write a Python function to reverse a string").
- Choose language, optimization focus, and options.
- Click **Generate Code**.
- Copy, download, or export the generated code.

### Code Explanation
- Select **Code Explanation**.
- Paste code or upload a file.
- Choose explanation detail level and focus areas.
- Click **Explain Code**.
- Read the explanation, download it, or ask follow-up questions.

### Learning Mode
- Select **Interactive Learning**.
- Pick a main topic and subtopic.
- Choose your preferred language, difficulty, and framework (if AI).
- Follow the interactive tutorial or quiz.

## Tips

- Use session history to revisit previous explanations and code.
- Adjust settings for a personalized experience.
- Use tooltips for guidance on each input.
- Download explanations and code in Markdown or plain text.