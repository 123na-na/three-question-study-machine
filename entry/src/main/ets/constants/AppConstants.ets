export interface ApiEndpoints {
  EVALUATE: string;
  SEARCH: string;
}

export interface ApiConfig {
  BASE_URL: string;
  ENDPOINTS: ApiEndpoints;
  TIMEOUT: number;
  STREAM_TIMEOUT: number;
}

export const API_CONFIG: ApiConfig = {
  // For HarmonyOS emulator, use 10.0.2.2 to access host machine
  // For real device, use your computer's LAN IP (e.g., 192.168.x.x)
  BASE_URL: 'http://10.0.2.2:8000',
  ENDPOINTS: {
    EVALUATE: '/api/v1/evaluate',
    SEARCH: '/api/v1/search'
  },
  TIMEOUT: 60000,
  STREAM_TIMEOUT: 120000
};

export const LEARNING_STEPS: string[] = ['what', 'why', 'how'];

export interface StepLabels {
  what: string;
  why: string;
  how: string;
}

export const STEP_LABELS: StepLabels = {
  what: '是什么',
  why: '为什么',
  how: '怎么用'
};

export interface MasteryLevel {
  min: number;
  max: number;
  label: string;
  color: string;
}

export interface MasteryLevels {
  EXCELLENT: MasteryLevel;
  GOOD: MasteryLevel;
  SATISFACTORY: MasteryLevel;
  NEEDS_REVIEW: MasteryLevel;
}

export const MASTERY_LEVELS: MasteryLevels = {
  EXCELLENT: { min: 90, max: 100, label: '优秀', color: '#52c41a' },
  GOOD: { min: 75, max: 89, label: '良好', color: '#1890ff' },
  SATISFACTORY: { min: 60, max: 74, label: '合格', color: '#faad14' },
  NEEDS_REVIEW: { min: 0, max: 59, label: '需复习', color: '#ff4d4f' }
};

export interface ScoreWeights {
  what: number;
  why: number;
  how: number;
}

export const SCORE_WEIGHTS: ScoreWeights = {
  what: 0.3,
  why: 0.35,
  how: 0.35
};
