import * as vscode from 'vscode';
import { Logger } from './utils/logger';
import { explainCode } from './commands/explain';
import { generateCode } from './commands/generate';
import { SynthexGhostTextProvider } from './providers/GhostTextProvider';
import { SynthexCodeActionProvider } from './providers/CodeActionProvider';

export function activate(context: vscode.ExtensionContext) {
    Logger.log('Synthex VS Code Extension is now active!');

    // Register Commands
    let explainDisposable = vscode.commands.registerCommand('synthex.explainCode', () => {
        explainCode(context);
    });

    let generateDisposable = vscode.commands.registerCommand('synthex.generateCode', () => {
        generateCode(context);
    });

    // Register Providers
    const ghostTextProvider = vscode.languages.registerInlineCompletionItemProvider(
        { pattern: '**' }, // Apply to all files
        new SynthexGhostTextProvider()
    );

    const codeActionProvider = vscode.languages.registerCodeActionsProvider(
        { pattern: '**' },
        new SynthexCodeActionProvider()
    );

    context.subscriptions.push(explainDisposable);
    context.subscriptions.push(generateDisposable);
    context.subscriptions.push(ghostTextProvider);
    context.subscriptions.push(codeActionProvider);
}

export function deactivate() {}
