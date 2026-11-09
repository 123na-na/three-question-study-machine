import { SCORE_WEIGHTS } from '../constants/AppConstants';

export function calculateOverallScore(stepScores: Record<string, number>): number {
  let totalWeight = 0;
  let weightedSum = 0;
  if (stepScores['what'] !== undefined) {
    weightedSum += stepScores['what'] * SCORE_WEIGHTS.what;
    totalWeight += SCORE_WEIGHTS.what;
  }
  if (stepScores['why'] !== undefined) {
    weightedSum += stepScores['why'] * SCORE_WEIGHTS.why;
    totalWeight += SCORE_WEIGHTS.why;
  }
  if (stepScores['how'] !== undefined) {
    weightedSum += stepScores['how'] * SCORE_WEIGHTS.how;
    totalWeight += SCORE_WEIGHTS.how;
  }
  if (totalWeight === 0) {
    return 0;
  }
  return Math.round(weightedSum / totalWeight);
}

interface MasteryResult { label: string; color: string }

export function getMasteryLevel(score: number): MasteryResult {
  if (score >= 90) return { label: 'mastered', color: '#52c41a' };
  if (score >= 75) return { label: 'proficient', color: '#1890ff' };
  if (score >= 60) return { label: 'familiar', color: '#faad14' };
  return { label: 'needs_review', color: '#ff4d4f' };
}
