# 🚀 Deployment & Publishing Guide

This guide covers how to host your Synthex API and publish your VS Code extension to the Marketplace.

---

## 🌍 Part 1: Hosting the FastAPI Backend

Since your extension relies on the Python backend, you need to host it online so users don't have to run it locally.

### Option A: Render (Easiest & Free Tier)

1.  **Push to GitHub**: Ensure your `Synthex` project is in a GitHub repository.
2.  **Sign up**: Go to [render.com](https://render.com) and login with GitHub.
3.  **Create Web Service**:
    - Click **New +** -> **Web Service**.
    - Select your repository.
4.  **Configure**:
    - **Name**: `synthex-api`
    - **Runtime**: `Python 3`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
5.  **Environment Variables**:
    - Add `GROQ_API_KEY` with your key.
6.  **Deploy**: Click "Create Web Service".
7.  **Get URL**: Copy your new URL (e.g., `https://synthex-api.onrender.com`).

### Option B: Railway (Good Alternative)

1.  Go to [railway.app](https://railway.app).
2.  "Start a New Project" -> "Deploy from GitHub repo".
3.  Add variables (`GROQ_API_KEY`) in the "Variables" tab.
4.  Railway automatically detects `requirements.txt` and `Procfile` (create a `Procfile` with `web: uvicorn main:app --host 0.0.0.0 --port $PORT` if needed).

---

## 📦 Part 2: Publishing the Extension

Now that your API is online, update the extension to use it by default.

### 1. Update Configuration

In `vscode-extension/package.json`, change the default API URL:

```json
"synthex.apiUrl": {
  "type": "string",
  "default": "https://your-render-app-name.onrender.com/api",
  "description": "URL of the running Synthex API"
}
```

### 2. Create a Marketplace Page (README)

Your `README.md` is your store page! Make it look professional.

- **Banner**: Add a cool banner image at the top.
- **GIFs**: Record a screen capture of you using "Explain" and "Generate" (use a tool like ScreenToGif).
- **Features List**: Use emojis and bullet points.

### 3. Package & Publish

1.  **Install vsce**: `npm install -g vsce`
2.  **Login**: `vsce login <publisher-id>` (Create one at [marketplace.visualstudio.com](https://marketplace.visualstudio.com/manage))
3.  **Publish**: `vsce publish`

---

## 🎨 Making a "Pro" Extension Page

To make your extension page look like the top ones:

1.  **Icon**: Create a 128x128 PNG logo. Set it in `package.json`: `"icon": "images/icon.png"`.
2.  **Badges**: Add shields.io badges to your README (e.g., version, downloads).
3.  **Categories**: In `package.json`, set `"categories": ["Programming Languages", "Machine Learning", "Education"]`.
4.  **Keywords**: Add keywords like `["python", "ai", "copilot", "chatgpt"]` to help people find it.

### Example `package.json` additions:

```json
"icon": "images/logo.png",
"publisher": "your-username",
"repository": {"type": "git", "url": "https://github.com/yourname/synthex"},
"keywords": ["ai", "coding", "assistant", "python", "explanation"],
```
