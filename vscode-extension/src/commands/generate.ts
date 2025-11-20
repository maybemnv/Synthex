import * as vscode from 'vscode';
import { SynthexApiClient } from '../api/client';
import { Logger } from '../utils/logger';

export async function generateCode(context: vscode.ExtensionContext) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found');
        return;
    }

    // 1. Get the description from the user
    const description = await vscode.window.showInputBox({
        placeHolder: 'e.g., Create a function to calculate Fibonacci numbers',
        prompt: 'Describe the code you want to generate'
    });

    if (!description) {
        return; // User cancelled
    }

    // 2. Show loading indicator
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Synthex: Generating code...",
        cancellable: false
    }, async (progress) => {
        try {
            const client = new SynthexApiClient();
            const language = editor.document.languageId;

            // 3. Call API
            const response = await client.generateCode(description, language);

            if (response.success && response.data.generated_code) {
                // 4. Insert code at cursor
                editor.edit(editBuilder => {
                    const position = editor.selection.active;
                    editBuilder.insert(position, response.data.generated_code);
                });
                
                Logger.log(`Generated code for: ${description}`);
            } else {
                const errorMsg = response.error || 'Unknown error occurred';
                Logger.error(`Generation failed: ${errorMsg}`);
                vscode.window.showErrorMessage(`Synthex Error: ${errorMsg}`);
            }
        } catch (error: any) {
            Logger.error('Generation command failed', error);
            vscode.window.showErrorMessage(`Synthex Error: ${error.message}`);
        }
    });
}
