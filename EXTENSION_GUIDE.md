# 📘 Synthex VS Code Extension Guide

This guide explains how the Synthex VS Code extension works, how to fix common issues, and how to publish it.

## 🏗️ Architecture Overview

The extension follows a **Client-Server** architecture:

1.  **Client (VS Code Extension)**: Written in TypeScript. It runs inside VS Code, listens for user actions (typing, commands), and displays results.
2.  **Server (Python API)**: Your existing FastAPI backend. It handles the heavy lifting (calling the LLM, parsing code).

### 📂 Folder Structure (`vscode-extension/src`)

- **`api/`**: Contains `client.ts`. This is the "bridge" between VS Code and your Python backend. It uses `axios` to send HTTP requests.
- **`commands/`**: Contains `explain.ts`. This handles the "Synthex: Explain Selection" command.
- **`providers/`**: Contains the "smart" features:
  - `GhostTextProvider.ts`: Watches what you type and asks the API for code suggestions (Ghost Text).
  - `CodeActionProvider.ts`: Adds the "Lightbulb" menu to explain code or fix errors.
- **`views/`**: Contains `SynthexPanel.ts`. This manages the side panel (Webview) that displays explanations.
- **`utils/`**: Helpers like `logger.ts` for debugging.

---

## 🔧 Troubleshooting "API Handler Not Initialized"

The error `API handler is not initialized` usually means the extension cannot talk to the Python backend or the Backend is misconfigured.

**Steps to Fix:**

1.  **Check the Backend**:

    - Ensure your Python server is running: `uvicorn main:app --reload --port 8000`
    - Ensure your `.env` file has the `GROQ_API_KEY`.
    - Test the API manually: Open `http://localhost:8000/docs` and try the `/api/generate` endpoint.

2.  **Check the Extension Config**:

    - In VS Code, go to **Settings** (`Ctrl+,`).
    - Search for `Synthex`.
    - Ensure `Api Url` is set to `http://localhost:8000/api`.

3.  **Check Logs**:
    - In VS Code, go to **Output** panel (`Ctrl+Shift+U`).
    - Select **Synthex** from the dropdown.
    - Look for specific error messages (e.g., "Connection refused").

---

## 🚀 How to Publish to Marketplace

Publishing allows anyone to install your extension.

### 1. Prepare for Release

- **Update `package.json`**:
  - Set a real `version` (e.g., `1.0.0`).
  - Add a good `icon` (128x128 png).
  - Fill in `publisher` (your username).
- **Create a README**: Ensure `README.md` has screenshots and instructions.

### 2. Install `vsce`

The "Visual Studio Code Extensions" CLI tool packages your extension.

```bash
npm install -g vsce
```

### 3. Package the Extension

Run this command to create a `.vsix` file (installable file):

```bash
vsce package
```

- _Note: You can send this `.vsix` file to friends to install manually!_

### 4. Publish to Marketplace

1.  Create a Microsoft account.
2.  Go to [Azure DevOps](https://dev.azure.com/) and create a **Personal Access Token (PAT)**.
3.  Create a publisher ID at [VS Code Marketplace Management](https://marketplace.visualstudio.com/manage).
4.  Login with `vsce`:
    ```bash
    vsce login <publisher id>
    ```
5.  Publish:
    ```bash
    vsce publish
    ```

### 💸 Is it Free?

**Yes!** Publishing to the VS Code Marketplace is 100% free.
