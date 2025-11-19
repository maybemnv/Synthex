"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Logger = void 0;
const vscode = require("vscode");
class Logger {
    static get channel() {
        if (!this._channel) {
            this._channel = vscode.window.createOutputChannel("Synthex");
        }
        return this._channel;
    }
    static log(message) {
        this.channel.appendLine(`[INFO] ${new Date().toLocaleTimeString()} - ${message}`);
    }
    static error(message, error) {
        this.channel.appendLine(`[ERROR] ${new Date().toLocaleTimeString()} - ${message}`);
        if (error) {
            this.channel.appendLine(JSON.stringify(error, null, 2));
        }
    }
}
exports.Logger = Logger;
//# sourceMappingURL=logger.js.map