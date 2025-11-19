import * as vscode from 'vscode';

export class Logger {
    private static _channel: vscode.OutputChannel;

    static get channel(): vscode.OutputChannel {
        if (!this._channel) {
            this._channel = vscode.window.createOutputChannel("Synthex");
        }
        return this._channel;
    }

    static log(message: string) {
        this.channel.appendLine(`[INFO] ${new Date().toLocaleTimeString()} - ${message}`);
    }

    static error(message: string, error?: any) {
        this.channel.appendLine(`[ERROR] ${new Date().toLocaleTimeString()} - ${message}`);
        if (error) {
            this.channel.appendLine(JSON.stringify(error, null, 2));
        }
    }
}
