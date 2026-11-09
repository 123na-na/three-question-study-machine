import { MASTERY_LEVELS, SCORE_WEIGHTS, MasteryLevel } from '../constants/AppConstants';

export class ScoreCalculator {
  static calculateOverallScore(whatScore: number, whyScore: number, howScore: number): number {
    return Math.round(
      whatScore * SCORE_WEIGHTS.what +
      whyScore * SCORE_WEIGHTS.why +
      howScore * SCORE_WEIGHTS.how
    );
  }

  static getMasteryLevel(score: number): MasteryLevel {
    if (score >= MASTERY_LEVELS.EXCELLENT.min) {
      return MASTERY_LEVELS.EXCELLENT;
    } else if (score >= MASTERY_LEVELS.GOOD.min) {
      return MASTERY_LEVELS.GOOD;
    } else if (score >= MASTERY_LEVELS.SATISFACTORY.min) {
      return MASTERY_LEVELS.SATISFACTORY;
    } else {
      return MASTERY_LEVELS.NEEDS_REVIEW;
    }
  }
}
