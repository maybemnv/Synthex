<div align="center">

# 🤖 Synthex

_Your AI-Powered Coding Companion_

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/your-username/synthex)
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0-red)](https://streamlit.io/)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](https://codecov.io)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

## 🎯 Overview

Synthex is your advanced AI coding assistant that transforms how developers understand, write, and learn code. Built with FastAPI and Streamlit, it leverages cutting-edge LLMs to provide:

- 📚 **Smart Code Explanations** - Detailed breakdowns with complexity analysis
- ⚡ **Intelligent Code Generation** - From natural language to optimized code
- 🎓 **Interactive Learning** - Personalized programming tutorials and challenges

## ✨ Key Features

### 1. Code Explanation Engine

- Line-by-line code analysis
- Time & space complexity insights
- Best practices recommendations
- Multi-language support

### 2. Code Generation

- Natural language to code conversion
- Optimization suggestions
- Template-based generation
- Context-aware completions

### 3. Learning Platform

- Interactive tutorials
- Hands-on challenges
- Progress tracking
- Real-world examples

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.9+
Git
Groq API key
```

### Installation

```bash
# Clone repository
git clone https://github.com/your-username/synthex.git
cd synthex

# Setup environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
Add your GROQ_API_KEY to .env
```

### Running Locally

```bash
# Start backend
uvicorn main:app --reload --port 8000

# Start frontend (new terminal)
streamlit run app.py
```

Access:

- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

## 📚 Documentation

- [API Reference](Documentation/API.md)
- [User Guide](Documentation/Useage.md)
- [Architecture Guide](Documentation/Architercture%20Guide.md)

## 📈 Performance

- Response Time: < 500ms+
- Code Analysis Accuracy: 95%+

## 🔮 Future Improvements

Planned enhancements for Synthex include:

- **Multi-LLM Support:** Integrate additional large language models (e.g., OpenAI GPT, Anthropic Claude) for fallback and response comparison.
- **VS Code Extension:** Develop a Visual Studio Code extension with features like inline ghost suggestions, contextual commands, and command palette integration for seamless in-editor AI assistance.
- **Advanced/Nice-to-Have Features:**
  - Progress tracker for learning mode and topic completion
  - Git diff explanation (explain code changes directly from version control)
  - Integration with communication tools (Slack, Discord, Teams)

## 🤝 Contributing

1. Fork the repo
2. Create your branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📄 License

[MIT License](LICENSE) - feel free to use this project as you wish.
