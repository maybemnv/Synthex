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
exports.explainCode = explainCode;
const vscode = require("vscode");
const client_1 = require("../api/client");
const SynthexPanel_1 = require("../views/SynthexPanel");
const logger_1 = require("../utils/logger");
function explainCode(context) {
    return __awaiter(this, void 0, void 0, function* () {
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
        }, (progress) => __awaiter(this, void 0, void 0, function* () {
            const client = new client_1.SynthexApiClient();
            const language = editor.document.languageId;
            const response = yield client.explainCode(text, language);
            if (response.success) {
                SynthexPanel_1.SynthexPanel.createOrShow(context.extensionUri);
                if (SynthexPanel_1.SynthexPanel.currentPanel) {
                    SynthexPanel_1.SynthexPanel.currentPanel.updateContent(response.data.explanation);
                }
            }
            else {
                logger_1.Logger.error(`Synthex Error: ${response.error}`);
                vscode.window.showErrorMessage(`Synthex Error: ${response.error}`);
            }
        }));
    });
}
//# sourceMappingURL=explain.js.map