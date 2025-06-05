# Synthex API Reference

## /api/status
- **GET**  
  Returns:  
  ```json
  { "success": true, "data": { "status": "online", "version": "1.0.0" } }
  ```

## /api/explain
- **POST**  
  **Body:**  
  ```json
  {
    "code": "string",
    "language": "python|cpp|java|...",
    "focus_areas": ["Algorithm Steps", ...],
    "difficulty": "Beginner|Intermediate|Advanced",
    "include_examples": true,
    "line_by_line": false
  }
  ```
  **Returns:**  
  ```json
  { "success": true, "data": { "explanation": "..." } }
  ```

### /api/explain/file
- **POST** (multipart/form-data)  
  Upload a code file for explanation.  
  **Fields:**  
    - `file`: code file (.py, .js, .cpp, etc.)
    - `difficulty`: (optional) string
    - `focus_areas`: (optional) comma-separated string
    - `line_by_line`: (optional) bool
    - `include_examples`: (optional) bool
  **Returns:**  
  ```json
  {
    "success": true,
    "data": {
      "explanation": "...",
      "filename": "example.py",
      "detected_language": "python",
      "file_stats": { "lines": 42, "characters": 1234, "size_kb": 3.2 }
    }
  }
  ```

### /api/explain/batch
- **POST** (multipart/form-data)  
  Upload multiple files for batch explanation.  
  **Fields:**  
    - `files`: list of code files
    - `difficulty`, `focus_areas`: as above
  **Returns:**  
  ```json
  {
    "success": true,
    "data": {
      "batch_results": [ ... ],
      "total_files": 2,
      "successful": 2,
      "failed": 0
    }
  }
  ```

### /api/explain/supported-types
- **GET**  
  Returns supported file types and limits.

## /api/generate
- **POST**  
  **Body:**  
  ```json
  {
    "description": "string",
    "language": "python|cpp|java|...",
    "difficulty": "Beginner|Intermediate|Advanced",
    "options": {
      "include_comments": true,
      "optimization_focus": "speed|memory|readability|balance"
    }
  }
  ```
  **Returns:**  
  ```json
  {
    "success": true,
    "data": {
      "generated_code": "...",
      "time_complexity": "O(n)",
      "space_complexity": "O(1)"
    }
  }
  ```

## /api/learn
- **POST**  
  **Body:**  
  ```json
  {
    "main_topic": "string",
    "subtopic": "string",
    "difficulty": "Beginner|Intermediate|Advanced",
    "language": "python|cpp|java|...",
    "framework": "string (optional)",
    "provider": "string (optional)"
  }
  ```
  **Query Params:**  
    - `template`: "concept_explanation" | "interactive_tutorial" | ...  
    - `session_id`: string

  **Returns:**  
  ```json
  {
    "success": true,
    "data": {
      "lesson": "...",
      "context": [ ... ]
    }
  }
  ```

## Error Responses
All endpoints may return errors in this format:
```json
{ "success": false, "error": "Error message here" }
```