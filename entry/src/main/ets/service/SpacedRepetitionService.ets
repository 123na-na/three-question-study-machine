import { ReviewRecord } from '../model/DataModel';
import { getReviewRecord, saveReviewRecord } from './DatabaseHelper';

const MIN_INTERVAL = 1;
const MAX_INTERVAL = 365;
const EASE_FACTOR_MIN = 1.3;
const EASE_FACTOR_MAX = 3.5;
const EASE_FACTOR_INITIAL = 2.5;

interface ReviewResult {
  easeFactor: number;
  intervalDays: number;
  nextReviewDate: string;
}

export function calculateNextReview(score: number, currentEaseFactor: number, currentInterval: number, currentReviewCount: number): ReviewResult {
  let newEaseFactor = currentEaseFactor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02));
  newEaseFactor = Math.max(EASE_FACTOR_MIN, Math.min(EASE_FACTOR_MAX, newEaseFactor));

  let newInterval: number;
  if (currentReviewCount === 0) {
    newInterval = MIN_INTERVAL;
  } else if (currentReviewCount === 1) {
    newInterval = 6;
  } else {
    newInterval = Math.round(currentInterval * newEaseFactor);
  }
  newInterval = Math.max(MIN_INTERVAL, Math.min(MAX_INTERVAL, newInterval));

  const now = new Date();
  const nextDate = new Date(now.getTime() + newInterval * 24 * 60 * 60 * 1000);
  const nextReviewDate = nextDate.getFullYear() + '-' +
    String(nextDate.getMonth() + 1).padStart(2, '0') + '-' +
    String(nextDate.getDate()).padStart(2, '0');

  return { easeFactor: newEaseFactor, intervalDays: newInterval, nextReviewDate };
}

export async function processReviewResult(kpId: number, score: number): Promise<void> {
  const normalizedScore = Math.round(score / 20);
  let review: ReviewRecord | null = null;
  try {
    review = await getReviewRecord(kpId);
  } catch (_) {
    review = null;
  }
  const easeFactor = review ? review.ease_factor : EASE_FACTOR_INITIAL;
  const intervalDays = review ? review.interval_days : 0;
  const reviewCount = review ? review.review_count : 0;
  const avgScore = review ? review.avg_score : 0;

  const result = calculateNextReview(normalizedScore, easeFactor, intervalDays, reviewCount);
  const newAvgScore = reviewCount > 0 ? (avgScore * reviewCount + score) / (reviewCount + 1) : score;
  let newStatus = 'pending';
  if (score >= 80) {
    newStatus = 'mastered';
  } else if (normalizedScore < 3) {
    newStatus = 'overdue';
  }
  await saveReviewRecord(kpId, result.easeFactor, result.intervalDays, result.nextReviewDate, reviewCount + 1, newAvgScore, newStatus);
}
