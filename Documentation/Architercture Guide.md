# Synthex Architecture Guide

## Overview

Synthex is a two-part application:
- **Frontend:** Streamlit app ([app.py](app.py)), with modular pages and UI components.
- **Backend:** FastAPI server ([main.py](main.py)), with modular API routes.

## Key Modules

- **Frontend**
  - `pages/`: Home, Generate, Explain, Learn
  - `components/`: UI widgets (code editor, theme, settings, etc.)
  - `utils/`: State management, API service, file handling, formatting

- **Backend**
  - `api/routes/`: API endpoints for explain, generate, learn
  - `api/services/`: LLM provider abstraction
  - `api/models/schemas.py`: Pydantic models for requests/responses

## Data Flow

1. **User interacts with Streamlit UI**
2. **Frontend calls FastAPI endpoints** via HTTP (see [API Reference](Documentation/API.md))
3. **Backend processes request** (calls LLM, parses, returns result)
4. **Frontend displays results** and updates session state/history

## LLM Integration

- Uses Groq's Llama 3 by default (see `.env` for API key)
- Provider abstraction allows for future support of OpenAI, Anthropic, etc.

## Session & Context

- Learning mode uses session IDs to track context for interactive lessons.
- History is stored in Streamlit session state for user review.

## File Handling

- File uploads are validated for type and size.
- Explanations can be generated for single or multiple files.

## Extensibility

- Add new providers by extending [`LLMProvider`](api/services/llm_provider.py)
- Add new UI features via `components/` and `pages/`
- Add new API endpoints in `api/routes/`