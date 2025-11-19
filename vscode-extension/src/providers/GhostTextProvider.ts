import * as vscode from 'vscode';
import { SynthexApiClient } from '../api/client';
import { Logger } from '../utils/logger';

export class SynthexGhostTextProvider implements vscode.InlineCompletionItemProvider {
    private client: SynthexApiClient;
    private debounceTimer: NodeJS.Timeout | undefined;

    constructor() {
        this.client = new SynthexApiClient();
    }

    async provideInlineCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        context: vscode.InlineCompletionContext,
        token: vscode.CancellationToken
    ): Promise<vscode.InlineCompletionItem[] | undefined> {
        
        // Only trigger if the user pauses for a bit (simple debounce logic would be handled by VS Code mostly, but we can add checks)
        // For now, let's trigger on specific patterns or just return undefined to not spam the API in this demo
        // In a real app, you'd want sophisticated triggering logic.
        
        const linePrefix = document.lineAt(position.line).text.substr(0, position.character);
        
        // Trigger if the line ends with a comment asking for code, e.g., "# generate: sort list"
        const triggerMatch = linePrefix.match(/(?:\/\/|#)\s*generate:\s*(.*)$/);
        
        if (!triggerMatch) {
            return undefined;
        }

        const description = triggerMatch[1];
        const language = document.languageId;

        Logger.log(`Ghost Text triggered for: ${description}`);

        try {
            const response = await this.client.generateCode(description, language);
            
            if (response.success && response.data.generated_code) {
                return [new vscode.InlineCompletionItem(
                    response.data.generated_code,
                    new vscode.Range(position, position)
                )];
            }
        } catch (e: any) {
            Logger.error("Ghost text generation failed");
            if (e.response) {
                Logger.error(`API Status: ${e.response.status}`);
                Logger.error(`API Data: ${JSON.stringify(e.response.data)}`);
            } else {
                Logger.error(`Error details: ${e.message}`);
            }
        }

        return undefined;
    }
}
