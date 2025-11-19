"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.SynthexGhostTextProvider = void 0;
const vscode = require("vscode");
const client_1 = require("../api/client");
const logger_1 = require("../utils/logger");
class SynthexGhostTextProvider {
    constructor() {
        this.client = new client_1.SynthexApiClient();
    }
    provideInlineCompletionItems(document, position, context, token) {
        return __awaiter(this, void 0, void 0, function* () {
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
            logger_1.Logger.log(`Ghost Text triggered for: ${description}`);
            try {
                const response = yield this.client.generateCode(description, language);
                if (response.success && response.data.generated_code) {
                    return [new vscode.InlineCompletionItem(response.data.generated_code, new vscode.Range(position, position))];
                }
            }
            catch (e) {
                logger_1.Logger.error("Ghost text generation failed", e);
            }
            return undefined;
        });
    }
}
exports.SynthexGhostTextProvider = SynthexGhostTextProvider;
//# sourceMappingURL=GhostTextProvider.js.map