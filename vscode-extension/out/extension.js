"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const logger_1 = require("./utils/logger");
const explain_1 = require("./commands/explain");
const GhostTextProvider_1 = require("./providers/GhostTextProvider");
const CodeActionProvider_1 = require("./providers/CodeActionProvider");
function activate(context) {
    logger_1.Logger.log('Synthex VS Code Extension is now active!');
    // Register Commands
    let explainDisposable = vscode.commands.registerCommand('synthex.explainCode', () => {
        (0, explain_1.explainCode)(context);
    });
    let generateDisposable = vscode.commands.registerCommand('synthex.generateCode', () => {
        vscode.window.showInformationMessage('Code Generation coming soon!');
    });
    // Register Providers
    const ghostTextProvider = vscode.languages.registerInlineCompletionItemProvider({ pattern: '**' }, // Apply to all files
    new GhostTextProvider_1.SynthexGhostTextProvider());
    const codeActionProvider = vscode.languages.registerCodeActionsProvider({ pattern: '**' }, new CodeActionProvider_1.SynthexCodeActionProvider());
    context.subscriptions.push(explainDisposable);
    context.subscriptions.push(generateDisposable);
    context.subscriptions.push(ghostTextProvider);
    context.subscriptions.push(codeActionProvider);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map