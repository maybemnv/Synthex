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
exports.SynthexApiClient = void 0;
const axios_1 = require("axios");
const config_1 = require("../config");
class SynthexApiClient {
    get baseUrl() {
        return (0, config_1.getApiUrl)();
    }
    explainCode(code, language) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                const response = yield axios_1.default.post(`${this.baseUrl}/explain`, {
                    code,
                    language,
                    difficulty: "intermediate",
                    focus_areas: ["Logic Flow", "Key Concepts"],
                    line_by_line: false
                });
                return response.data;
            }
            catch (error) {
                console.error('API Error:', error);
                return {
                    success: false,
                    data: { explanation: '' },
                    error: error.message || 'Failed to connect to Synthex API'
                };
            }
        });
    }
    generateCode(description, language) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                const response = yield axios_1.default.post(`${this.baseUrl}/generate`, {
                    description,
                    language,
                    difficulty: "intermediate"
                });
                return response.data;
            }
            catch (error) {
                console.error('API Error:', error);
                return {
                    success: false,
                    data: { generated_code: '' },
                    error: error.message || 'Failed to connect to Synthex API'
                };
            }
        });
    }
}
exports.SynthexApiClient = SynthexApiClient;
//# sourceMappingURL=client.js.map