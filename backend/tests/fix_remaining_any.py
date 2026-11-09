"""Fix remaining ArkTS issues: any types and inline return types."""
import os, re

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

# ===== 1. SpacedRepetitionService.ets - inline return type =====
fp = os.path.join(BASE, 'service', 'SpacedRepetitionService.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Add ReviewResult interface
text = text.replace(
    'import { getReviewRecord, saveReviewRecord } from \'./DatabaseHelper\';',
    'import { getReviewRecord, saveReviewRecord } from \'./DatabaseHelper\';\n\ninterface ReviewResult {\n  easeFactor: number;\n  intervalDays: number;\n  nextReviewDate: string;\n}'
)

# Fix return type
text = text.replace(
    'export function calculateNextReview(score: number, currentEaseFactor: number, currentInterval: number, currentReviewCount: number): {\n  easeFactor: number;\n  intervalDays: number;\n  nextReviewDate: string;\n} {',
    'export function calculateNextReview(score: number, currentEaseFactor: number, currentInterval: number, currentReviewCount: number): ReviewResult {'
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: SpacedRepetitionService.ets')

# ===== 2. service/ScoreCalculator.ets - inline return type =====
fp = os.path.join(BASE, 'service', 'ScoreCalculator.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

text = text.replace(
    'export function getMasteryLevel(score: number): { label: string; color: string } {',
    'interface MasteryResult { label: string; color: string }\n\nexport function getMasteryLevel(score: number): MasteryResult {'
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: service/ScoreCalculator.ets')

# ===== 3. DatabaseHelper.ets - any[] in getReviewsDue =====
fp = os.path.join(BASE, 'service', 'DatabaseHelper.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Find function signature for getReviewsDue
# Add an interface for the return type
if 'interface ReviewDueItem' not in text:
    text = text.replace(
        'export async function getReviewsDue(): Promise<any[]> {',
        'interface ReviewDueItem {\n  id: number;\n  knowledge_point_id: number;\n  ease_factor: number;\n  interval_days: number;\n  next_review_date: string;\n  review_count: number;\n  avg_score: number;\n  kp_title: string;\n  course_name: string;\n}\n\nexport async function getReviewsDue(): Promise<ReviewDueItem[]> {'
    )

# Fix the items: any[] initialization
text = text.replace(
    'const items: any[] = [];',
    'const items: ReviewDueItem[] = [];'
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: DatabaseHelper.ets (any[] -> ReviewDueItem[])')

# ===== 4. ReviewTab.ets - any types =====
fp = os.path.join(BASE, 'component', 'ReviewTab.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Define ReviewDueItem interface (matching DatabaseHelper)
# @State reviewsDue: any[] = [];
text = text.replace(
    '@State reviewsDue: any[] = [];',
    '@State reviewsDue: ReviewDueItem[] = [];'
)

# ForEach with any
text = text.replace(
    "ForEach(this.reviewsDue, (item: any) => {",
    "ForEach(this.reviewsDue, (item: ReviewDueItem) => {"
)

# (item: any) => item.id.toString()
text = text.replace(
    "(item: any) => item.id.toString()",
    "(item: ReviewDueItem) => item.id.toString()"
)

# item: any = {};
# Sub-component property
text = text.replace(
    'item: any = {};',
    'item: ReviewDueItem | null = null;'
)

# Also need to add the import/interface for ReviewDueItem
# Check if already defined or imported
if 'ReviewDueItem' in text and 'import' not in text:
    # Add interface
    text = text.replace(
        '@State reviewsDue: ReviewDueItem[] = [];',
        'interface ReviewDueItem {\n  id: number;\n  knowledge_point_id: number;\n  ease_factor: number;\n  interval_days: number;\n  next_review_date: string;\n  review_count: number;\n  avg_score: number;\n  kp_title: string;\n  course_name: string;\n}\n\n  @State reviewsDue: ReviewDueItem[] = [];'
    )

# Fix toString call with null
text = text.replace(
    "(item: ReviewDueItem) => item.id.toString()",
    "(item: ReviewDueItem) => String(item.id)"
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: ReviewTab.ets')

# ===== 5. ProgressDashboardPage.ets - any types =====
fp = os.path.join(BASE, 'pages', 'ProgressDashboardPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Find: ForEach(getAchievementDefs(), (def: any) => {
text = text.replace(
    "ForEach(getAchievementDefs(), (def: any) => {",
    "ForEach(getAchievementDefs(), (def: AchievementDef) => {"
)

# Find: ForEach(getUnlockedAchievements(), (ach: any) => {
text = text.replace(
    "ForEach(getUnlockedAchievements(), (ach: any) => {",
    "ForEach(getUnlockedAchievements(), (ach: Achievement) => {"
)

# Add import for Achievement
text = text.replace(
    "import { Colors, Spacing, Radius } from '../constants/Theme';",
    "import { Colors, Spacing, Radius } from '../constants/Theme';\nimport { Achievement } from '../model/DataModel';"
)

# Add AchievementDef import
if 'AchievementDef' not in text:
    text = text.replace(
        "import { Achievement } from '../model/DataModel';",
        "import { Achievement, AchievementDef } from '../model/DataModel';"
    )

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: ProgressDashboardPage.ets')

# ===== 6. ShareUtil.ets - any return type =====
fp = os.path.join(BASE, 'service', 'ShareUtil.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# function getPastable(): any {
# Replace with more specific type
text = text.replace(
    'function getPastable(): any {',
    'function getPastable(): ShareData {'
)

# Add ShareData interface if not present
if 'interface ShareData' not in text:
    text = text.replace(
        "import { common } from '@kit.AbilityKit';",
        "import { common } from '@kit.AbilityKit';\n\ninterface ShareData {\n  title: string;\n  content: string;\n  image?: string;\n}"
    )

# Fix other any types in the file
text = text.replace(
    'data: any',
    'data: ShareData'
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: ShareUtil.ets')

print('\nAll remaining fixes applied.')
