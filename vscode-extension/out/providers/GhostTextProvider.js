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
const vscode = __importStar(require("vscode"));
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
                logger_1.Logger.error("Ghost text generation failed");
                if (e.response) {
                    logger_1.Logger.error(`API Status: ${e.response.status}`);
                    logger_1.Logger.error(`API Data: ${JSON.stringify(e.response.data)}`);
                }
                else {
                    logger_1.Logger.error(`Error details: ${e.message}`);
                }
            }
            return undefined;
        });
    }
}
exports.SynthexGhostTextProvider = SynthexGhostTextProvider;
//# sourceMappingURL=GhostTextProvider.js.map