import axios from 'axios';
import { getApiUrl } from '../config';

export interface ExplainResponse {
    success: boolean;
    data: {
        explanation: string;
        processing_time?: number;
    };
    error?: string;
}

export class SynthexApiClient {
    private get baseUrl(): string {
        return getApiUrl();
    }

    async explainCode(code: string, language: string): Promise<ExplainResponse> {
        try {
            const response = await axios.post(`${this.baseUrl}/explain`, {
                code,
                language,
                difficulty: "intermediate",
                focus_areas: ["Logic Flow", "Key Concepts"],
                line_by_line: false
            });
            return response.data;
        } catch (error: any) {
            console.error('API Error:', error);
            return {
                success: false,
                data: { explanation: '' },
                error: error.message || 'Failed to connect to Synthex API'
            };
        }
    }

    async generateCode(description: string, language: string): Promise<{ success: boolean; data: { generated_code: string }; error?: string }> {
        try {
            const response = await axios.post(`${this.baseUrl}/generate`, {
                description,
                language,
                difficulty: "intermediate"
            });
            return response.data;
        } catch (error: any) {
            console.error('API Error:', error);
            return {
                success: false,
                data: { generated_code: '' },
                error: error.message || 'Failed to connect to Synthex API'
            };
        }
    }
}
