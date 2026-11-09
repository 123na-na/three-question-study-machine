"""
Unit tests for core business logic:
- ScoreCalculator (weighted scoring, mastery levels)
- SM-2 spaced repetition algorithm
"""
import math
import sys

# ===== ScoreCalculator tests =====
SCORE_WEIGHTS = {'what': 0.3, 'why': 0.35, 'how': 0.35}

def calculate_overall_score(what_score, why_score, how_score):
    return round(
        what_score * SCORE_WEIGHTS['what'] +
        why_score * SCORE_WEIGHTS['why'] +
        how_score * SCORE_WEIGHTS['how']
    )

MASTERY_LEVELS = [
    ('EXCELLENT', 90, 100, '优秀'),
    ('GOOD', 75, 89, '良好'),
    ('SATISFACTORY', 60, 74, '合格'),
    ('NEEDS_REVIEW', 0, 59, '需复习'),
]

def get_mastery_level(score):
    for _, lo, hi, label in MASTERY_LEVELS:
        if lo <= score <= hi:
            return label
    return '需复习'


def test_score_calculator():
    cases = [
        (90, 95, 85, '优秀'),
        (80, 78, 82, '良好'),
        (65, 70, 60, '合格'),
        (40, 50, 45, '需复习'),
        (100, 100, 100, '优秀'),
        (0, 0, 0, '需复习'),
    ]
    for what, why, how, expected in cases:
        score = calculate_overall_score(what, why, how)
        label = get_mastery_level(score)
        assert label == expected, f"({what},{why},{how}) => {score}pts = {label}, expected {expected}"
    print(f"  ScoreCalculator: {len(cases)} cases passed")


# ===== SM-2 Algorithm tests =====
def sm2_calculate(ease_factor, interval_days, review_count, score):
    if score >= 80:
        new_ef = ease_factor + 0.1
        if review_count == 0:
            new_interval = 1
        elif review_count == 1:
            new_interval = 6
        else:
            new_interval = round(interval_days * ease_factor)
    elif score >= 60:
        new_ef = ease_factor
        if review_count == 0:
            new_interval = 1
        else:
            new_interval = interval_days
    else:
        new_ef = ease_factor - 0.2
        new_interval = 1
    new_ef = max(1.3, min(3.0, new_ef))
    new_interval = max(1, min(new_interval, 365))
    return new_ef, new_interval


def test_sm2():
    cases = [
        (2.5, 0, 0, 85, 2.6, 1),     # good score, first review
        (2.6, 1, 1, 85, 2.7, 6),     # good score, second review
        (2.7, 6, 2, 85, 2.8, 16),    # good score, third => round(6*2.7)
        (2.5, 1, 1, 70, 2.5, 1),     # medium score, EF unchanged
        (2.5, 6, 2, 70, 2.5, 6),     # medium score, interval unchanged
        (2.5, 1, 1, 50, 2.3, 1),     # poor score, EF-0.2, interval=1
        (1.3, 0, 0, 50, 1.3, 1),     # EF clamped at min 1.3
        (3.0, 10, 2, 90, 3.0, 30),   # EF clamped at max 3.0, interval=round(10*3.0)
        (2.5, 200, 3, 85, 2.6, 365), # interval clamped at max 365
    ]
    for ef, interval, count, score, exp_ef, exp_int in cases:
        new_ef, new_int = sm2_calculate(ef, interval, count, score)
        assert abs(new_ef - exp_ef) < 0.01, f"EF mismatch: got {new_ef}, expected {exp_ef}"
        assert new_int == exp_int, f"Interval mismatch: got {new_int}, expected {exp_int}"
    print(f"  SM-2 Algorithm: {len(cases)} cases passed")


# ===== Average score calculation tests =====
def test_average_score():
    cases = [
        (0, 0, 85, 85),     # first score
        (1, 80, 90, 85),    # (80*1 + 90)/2
        (2, 80, 90, 83),    # (80*2 + 90)/3
        (1, 60, 40, 50),    # (60*1 + 40)/2
    ]
    for old_count, old_avg, score, expected in cases:
        result = round((old_avg * old_count + score) / (old_count + 1))
        assert result == expected, f"({old_count},{old_avg},{score}) => {result}, expected {expected}"
    print(f"  Average Score: {len(cases)} cases passed")


if __name__ == '__main__':
    print("Running unit tests...")
    test_score_calculator()
    test_sm2()
    test_average_score()
    print("All tests passed!")
