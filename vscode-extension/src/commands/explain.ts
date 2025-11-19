import * as vscode from 'vscode';
import { SynthexApiClient } from '../api/client';
import { SynthexPanel } from '../views/SynthexPanel';
import { Logger } from '../utils/logger';

export async function explainCode(context: vscode.ExtensionContext) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found');
        return;
    }

    const selection = editor.selection;
    const text = editor.document.getText(selection);

    if (!text) {
        vscode.window.showWarningMessage('Please select some code to explain');
        return;
    }

    // Show loading indicator
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Synthex: Analyzing code...",
        cancellable: false
    }, async (progress) => {
        const client = new SynthexApiClient();
        const language = editor.document.languageId;
        
        const response = await client.explainCode(text, language);

        if (response.success) {
            SynthexPanel.createOrShow(context.extensionUri);
            if (SynthexPanel.currentPanel) {
                SynthexPanel.currentPanel.updateContent(response.data.explanation);
            }
        } else {
            Logger.error(`Synthex Error: ${response.error}`);
            vscode.window.showErrorMessage(`Synthex Error: ${response.error}`);
        }
    });
}
