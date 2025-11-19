import * as vscode from 'vscode';

export const getApiUrl = (): string => {
    const config = vscode.workspace.getConfiguration('synthex');
    return config.get<string>('apiUrl', 'http://localhost:8000/api');
};
