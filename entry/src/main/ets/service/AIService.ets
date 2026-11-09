import http from '@ohos.net.http';
import { API_CONFIG } from '../constants/AppConstants';
import { AIEvaluationResponse } from '../model/DataModel';
import { getPreference, setPreference } from './DatabaseHelper';

const PREF_BACKEND_URL = 'backend_url';

export async function getBaseUrl(): Promise<string> {
  const saved = await getPreference(PREF_BACKEND_URL);
  return saved || API_CONFIG.BASE_URL;
}

export async function setBaseUrl(url: string): Promise<void> {
  await setPreference(PREF_BACKEND_URL, url);
  API_CONFIG.BASE_URL = url;
}

export async function initFromPreferences(): Promise<void> {
  const saved = await getPreference(PREF_BACKEND_URL);
  if (saved) {
    API_CONFIG.BASE_URL = saved;
  }
}

export async function evaluateWithAI(question: string, userAnswer: string, step: string): Promise<AIEvaluationResponse> {
  const baseUrl = await getBaseUrl();
  const url = baseUrl + API_CONFIG.ENDPOINTS.EVALUATE;
  const httpRequest = http.createHttp();
  const body: Record<string, string> = { 'question': question, 'user_answer': userAnswer, 'step': step };
  const extraOpts: http.HttpRequestOptions = {
    method: http.RequestMethod.POST,
    header: { 'Content-Type': 'application/json' },
    extraData: JSON.stringify(body),
    connectTimeout: API_CONFIG.TIMEOUT,
    readTimeout: API_CONFIG.TIMEOUT,
  };
  return new Promise<AIEvaluationResponse>((resolve, reject) => {
    httpRequest.request(url, extraOpts, (err, data) => {
      httpRequest.destroy();
      if (err) {
        reject(new Error('HTTP ' + err.code + ': ' + err.message));
        return;
      }
      const code = data.responseCode;
      if (code !== 200) {
        reject(new Error('Server error: ' + code));
        return;
      }
      try {
        const result: AIEvaluationResponse = JSON.parse(data.result as string);
        resolve(result);
      } catch (e) {
        reject(new Error('Failed to parse AI response'));
      }
    });
  });
}

export function evaluateWithAIStream(onData: (chunk: string) => void, onDone: () => void, onError: (err: Error) => void): void {
  setTimeout(() => {
    onDone();
  }, 100);
}
