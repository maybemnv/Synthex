# Synthex User Guide

## Getting Started

1. **Launch the app:**  
   - Start backend: `uvicorn api.main:app --reload`
   - Start frontend: `streamlit run app.py`
2. **Navigate using the sidebar:**  
   - Select "Generate", "Explain", or "Learn" mode.

## Example Workflows

### Code Generation
- Select **Generate** mode.
- Enter a prompt (e.g., "Write a Python function to reverse a string").
- Choose language and optimization focus.
- Click **Generate Code**.
- Copy or review the generated code.

### Code Explanation
- Select **Explain** mode.
- Paste your code (e.g., `def fib(n): ...`).
- Choose explanation detail level and focus areas.
- Click **Explain Code**.
- Read the explanation and ask follow-up questions.

### Learning Mode
- Select **Learn** mode.
- Pick a main topic (e.g., "AI") and subtopic (e.g., "ML - Supervised Learning").
- Choose your preferred language and difficulty.
- Follow the interactive tutorial or quiz.

---

## Tips

- Use session history to revisit previous explanations and code.
- Adjust settings for a personalized experience.
- Use tooltips for guidance on each input.
