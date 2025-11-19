import * as vscode from 'vscode';

export class SynthexCodeActionProvider implements vscode.CodeActionProvider {
    provideCodeActions(
        document: vscode.TextDocument,
        range: vscode.Range | vscode.Selection,
        context: vscode.CodeActionContext,
        token: vscode.CancellationToken
    ): vscode.ProviderResult<(vscode.Command | vscode.CodeAction)[]> {
        
        const actions: vscode.CodeAction[] = [];

        // 1. Explain Selection Action
        if (!range.isEmpty) {
            const explainAction = new vscode.CodeAction(
                'Synthex: Explain this code',
                vscode.CodeActionKind.QuickFix
            );
            explainAction.command = {
                command: 'synthex.explainCode',
                title: 'Explain Code'
            };
            actions.push(explainAction);
        }

        // 2. Fix Error Action (if there are diagnostics)
        if (context.diagnostics.length > 0) {
            const fixAction = new vscode.CodeAction(
                'Synthex: Fix this error (Coming Soon)',
                vscode.CodeActionKind.QuickFix
            );
            fixAction.isPreferred = true;
            actions.push(fixAction);
        }

        return actions;
    }
}
