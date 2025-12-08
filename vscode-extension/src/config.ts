import * as vscode from 'vscode';

export const getApiUrl = (): string => {
    const config = vscode.workspace.getConfiguration('synthex');
    return config.get<string>('apiUrl', 'https://synthex-3.onrender.com/api');
};
