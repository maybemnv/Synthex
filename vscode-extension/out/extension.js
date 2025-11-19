"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
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