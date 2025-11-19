"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SynthexPanel = void 0;
const vscode = require("vscode");
class SynthexPanel {
    constructor(panel, extensionUri) {
        this._disposables = [];
        this._panel = panel;
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        this._panel.webview.html = this._getWebviewContent();
    }
    static createOrShow(extensionUri) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;
        if (SynthexPanel.currentPanel) {
            SynthexPanel.currentPanel._panel.reveal(column);
            return;
        }
        const panel = vscode.window.createWebviewPanel('synthex', 'Synthex AI', column || vscode.ViewColumn.One, {
            enableScripts: true,
            localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'media')]
        });
        SynthexPanel.currentPanel = new SynthexPanel(panel, extensionUri);
    }
    updateContent(content) {
        this._panel.webview.html = this._getWebviewContent(content);
    }
    dispose() {
        SynthexPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) {
                x.dispose();
            }
        }
    }
    _getWebviewContent(content = 'Select code and run "Synthex: Explain Selection" to see the magic!') {
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Synthex AI</title>
            <style>
                body {
                    font-family: var(--vscode-font-family);
                    padding: 20px;
                    color: var(--vscode-editor-foreground);
                    background-color: var(--vscode-editor-background);
                }
                h1 {
                    color: var(--vscode-textLink-foreground);
                }
                .content {
                    line-height: 1.6;
                    white-space: pre-wrap;
                }
            </style>
        </head>
        <body>
            <h1>Synthex Explanation</h1>
            <div class="content">${content}</div>
        </body>
        </html>`;
    }
}
exports.SynthexPanel = SynthexPanel;
//# sourceMappingURL=SynthexPanel.js.map