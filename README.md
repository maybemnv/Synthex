# Synthex: AI-Powered Coding Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Coverage](https://img.shields.io/badge/coverage-85%25-green)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Project Overview

Synthex is an advanced AI-powered coding assistant designed to revolutionize how developers understand, generate, and learn programming concepts. Built on a robust architecture combining FastAPI and Streamlit, this application leverages state-of-the-art language models to provide comprehensive code explanations, generate optimized code snippets, and deliver interactive learning experiences tailored to various programming domains.

## Core Functionality

The application serves three primary functions:

1. **Code Explanation Engine**: Parses and analyzes code snippets to generate detailed explanations including algorithm steps, time and space complexity analysis, and best practices recommendations.

2. **Intelligent Code Generation**: Transforms natural language prompts into syntactically correct, optimized code snippets across multiple programming languages with options for optimization parameters.

3. **Interactive Learning Platform**: Provides structured tutorials, challenges, and quizzes across programming topics including data structures, algorithms, AI fundamentals, OOP patterns, web development frameworks, and more.

## System Architecture

![System Architecture](https://via.placeholder.com/800x400?text=Synthex+Architecture+Diagram)

### Backend (FastAPI)

The backend implements a RESTful API architecture with the following components:

- **Route Handlers**: Process incoming requests and direct to appropriate service modules
- **Pydantic Models**: Define data validation schemas for request/response payloads
- **Service Layer**: Contains business logic and LLM integration mechanisms
- **Configuration Module**: Manages environment variables and application settings

### Frontend (Streamlit)

The frontend provides an intuitive user interface with:

- **Core Application**: Main dashboard and navigation structure
- **Feature Pages**: Dedicated interfaces for each major functionality
- **Reusable Components**: Custom UI elements for consistent user experience
- **Utility Modules**: Support functions for data processing and display

## Technology Stack

- **Backend Framework**: FastAPI
- **Frontend Framework**: Streamlit
- **AI Integration**: Groq API (Llama Models)
- **Testing**: Pytest with coverage reporting
- **Documentation**: Sphinx with autodoc
- **Containerization**: Docker with docker-compose
- **CI/CD**: GitHub Actions

## Project Structure

```
synthex/
├── app.py                 # Streamlit frontend application entry point
├── api/                   # FastAPI backend components
│   ├── main.py            # FastAPI entry point
│   ├── routes/            # API endpoint definitions
│   │   ├── __init__.py
│   │   ├── explain.py     # Code explanation endpoints
│   │   ├── generate.py    # Code generation endpoints
│   │   └── learn.py       # Learning content endpoints
│   ├── models/            # Pydantic schemas for data validation
│   │   ├── __init__.py
│   │   ├── requests.py    # Request models
│   │   └── responses.py   # Response models
│   ├── services/          # Business logic and LLM integration
│   │   ├── __init__.py
│   │   ├── llm_provider.py # LLM connection and prompt handling
│   │   ├── explainer.py   # Code explanation logic
│   │   ├── generator.py   # Code generation logic
│   │   └── tutor.py       # Learning content creation logic
│   └── config/            # Configuration and settings
│       ├── __init__.py
│       └── settings.py    # Environment and application settings
├── pages/                 # Streamlit pages for different features
│   ├── __init__.py
│   ├── explain.py         # Code explanation page
│   ├── generate.py        # Code generation page
│   └── learn.py           # Learning content page
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── code_formatter.py  # Code formatting utilities
│   └── session_manager.py # Session state management
├── components/            # Reusable UI components
│   ├── __init__.py
│   ├── code_editor.py     # Code editor component
│   └── result_display.py  # Results display component
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_backend.py    # Backend unit tests
│   ├── test_frontend.py   # Frontend unit tests
│   └── e2e/               # End-to-end test scenarios
│       ├── __init__.py
│       └── test_flows.py  # Complete user flow tests
├── documentation/         # Project documentation
│   ├── architecture.md    # System architecture documentation
│   ├── api_reference.md   # API reference documentation
│   └── tasks.txt          # Task tracking and roadmap
├── Dockerfile             # Docker containerization
├── docker-compose.yml     # Multi-container definition
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore patterns
└── README.md              # This file
```

## Installation and Setup

### Prerequisites

- Python 3.9+
- Git
- Virtual environment tool (venv, conda, etc.)
- Groq API key

### Development Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/synthex.git
   cd synthex
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate   # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file to add your GROQ_API_KEY
   ```

## Running the Application

### Development Mode

1. **Start the FastAPI backend:**
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

2. **Start the Streamlit frontend (in a separate terminal):**
   ```bash
   streamlit run app.py
   ```

3. **Access the application:**
   - Frontend: http://localhost:8501
   - API documentation: http://localhost:8000/docs

### Using Docker

```bash
docker-compose up -d
```

The application will be available at http://localhost:8501

## API Documentation

### Core Endpoints

| Endpoint | Method | Description | Request Payload | Response |
|----------|--------|-------------|----------------|----------|
| `/api/status` | GET | Service health check | None | `{"status": "ok", "version": "1.0.0"}` |
| `/api/explain` | POST | Explain code snippet | `{"code": "string", "language": "string", "detail_level": "string"}` | `{"explanation": "string", "complexity": "string", "best_practices": ["string"]}` |
| `/api/generate` | POST | Generate code from prompt | `{"prompt": "string", "language": "string", "optimization": "string"}` | `{"code": "string", "explanation": "string"}` |
| `/api/learn` | POST | Get learning content | `{"topic": "string", "difficulty": "string", "format": "string"}` | `{"content": "string", "exercises": ["string"]}` |

For detailed API documentation, run the application and visit http://localhost:8000/docs

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=api --cov=pages --cov-report=term-missing

# Run specific test categories
pytest tests/test_backend.py
pytest tests/test_frontend.py
pytest tests/e2e/
```

### Testing Strategy

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user flows
- **Coverage Target**: Minimum 80% code coverage

## Deployment

### Production Considerations

- Use gunicorn or similar WSGI server for FastAPI in production
- Configure proper CORS settings for production deployment
- Set up proper logging and monitoring
- Implement rate limiting for API endpoints

### Deployment Options

- **Cloud Platform Deployment**: AWS, GCP, or Azure with containerization
- **Self-Hosted**: Using Docker on VPS or dedicated server
- **Serverless**: AWS Lambda with API Gateway (requires adaptation)

## Future Development

- Advanced code analysis with AST parsing
- Multi-language support expansion
- User profile and progress tracking
- Collaborative coding sessions
- Custom model fine-tuning for programming-specific tasks

## Contributing

We welcome contributions from all developers. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows our coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the efficient API framework
- [Streamlit](https://streamlit.io/) for the intuitive UI framework
- [Groq](https://groq.com/) for providing access to Llama Models
- All open-source contributors and libraries used in this project
