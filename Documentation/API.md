# Synthex API Reference

## /api/status
- **GET**  
  Returns: `{ "success": true, ... }`

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
      "optimization_focus": "speed|memory|readability"
    }
  }
  ```
  **Returns:**  
  ```json
  { "success": true, "data": { "generated_code": "..." } }
  ```

## /api/learn
- **POST**  
  **Body:**  
  ```json
  {
    "topic": "string",
    "difficulty": "Beginner|Intermediate|Advanced",
    "language": "python|cpp|java|..."
  }
  ```
  **Returns:**  
  ```json
  { "success": true, "data": { "content": "..." } }
  ```

## Error Responses
All endpoints may return errors in this format:
```json
{ "success": false, "error": "Error message here" }
```
