"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SynthexCodeActionProvider = void 0;
const vscode = require("vscode");
class SynthexCodeActionProvider {
    provideCodeActions(document, range, context, token) {
        const actions = [];
        // 1. Explain Selection Action
        if (!range.isEmpty) {
            const explainAction = new vscode.CodeAction('Synthex: Explain this code', vscode.CodeActionKind.QuickFix);
            explainAction.command = {
                command: 'synthex.explainCode',
                title: 'Explain Code'
            };
            actions.push(explainAction);
        }
        // 2. Fix Error Action (if there are diagnostics)
        if (context.diagnostics.length > 0) {
            const fixAction = new vscode.CodeAction('Synthex: Fix this error (Coming Soon)', vscode.CodeActionKind.QuickFix);
            fixAction.isPreferred = true;
            actions.push(fixAction);
        }
        return actions;
    }
}
exports.SynthexCodeActionProvider = SynthexCodeActionProvider;
//# sourceMappingURL=CodeActionProvider.js.map