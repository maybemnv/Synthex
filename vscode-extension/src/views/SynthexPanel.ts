import * as vscode from 'vscode';

export class SynthexPanel {
    public static currentPanel: SynthexPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _disposables: vscode.Disposable[] = [];

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
        this._panel = panel;
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        this._panel.webview.html = this._getWebviewContent();
    }

    public static createOrShow(extensionUri: vscode.Uri) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        if (SynthexPanel.currentPanel) {
            SynthexPanel.currentPanel._panel.reveal(column);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'synthex',
            'Synthex AI',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'media')]
            }
        );

        SynthexPanel.currentPanel = new SynthexPanel(panel, extensionUri);
    }

    public updateContent(content: string) {
        this._panel.webview.html = this._getWebviewContent(content);
    }

    public dispose() {
        SynthexPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) {
                x.dispose();
            }
        }
    }

    private _getWebviewContent(content: string = 'Select code and run "Synthex: Explain Selection" to see the magic!') {
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
