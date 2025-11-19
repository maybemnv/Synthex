# Synthex VS Code Extension

This is the official VS Code extension for Synthex, your AI-powered coding companion.

## Features

- **Explain Code**: Select any code snippet, right-click, and choose "Synthex: Explain Selection".
- **Generate Code**: (Coming Soon) Generate code from natural language descriptions.

## Setup & Development

1.  **Prerequisites**:

    - Node.js installed.
    - The Synthex Python backend running locally on `http://localhost:8000`.

2.  **Installation**:

    ```bash
    cd vscode-extension
    npm install
    ```

3.  **Running the Extension**:

    - Open this folder (`vscode-extension`) in VS Code.
    - Press `F5` to start debugging.
    - A new VS Code window will open with the extension loaded.

4.  **Usage**:
    - Open a code file.
    - Select some code.
    - Right-click and select "Synthex: Explain Selection".
    - A panel will open with the AI explanation.

## Configuration

You can configure the API URL in VS Code Settings:

- `synthex.apiUrl`: Default is `http://localhost:8000/api`
