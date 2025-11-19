"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getApiUrl = void 0;
const vscode = require("vscode");
const getApiUrl = () => {
    const config = vscode.workspace.getConfiguration('synthex');
    return config.get('apiUrl', 'http://localhost:8000/api');
};
exports.getApiUrl = getApiUrl;
//# sourceMappingURL=config.js.map