"""Final fix pass for remaining ArkTS issues."""
import os, re

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

# ===== 1. AchievementService - export AchievementDef + fix return type =====
fp = os.path.join(BASE, 'service', 'AchievementService.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Export AchievementDef interface
text = text.replace(
    'interface AchievementDef {',
    'export interface AchievementDef {'
)

# Fix getAchievementDefs return type and body
text = text.replace(
    "export function getAchievementDefs(): Array<{ id: string; name: string; description: string; icon: string }> {\n  return ACHIEVEMENT_DEFS.map((def) => ({ id: def.id, name: def.name, description: def.description, icon: def.icon } as { id: string; name: string; description: string; icon: string }));\n}",
    "export function getAchievementDefs(): AchievementDef[] {\n  return ACHIEVEMENT_DEFS.map((def) => ({ id: def.id, name: def.name, description: def.description, icon: def.icon }));\n}"
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: AchievementService.ets')

# ===== 2. ProgressDashboardPage - fix any, private, userStats =====
fp = os.path.join(BASE, 'pages', 'ProgressDashboardPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Add imports
text = text.replace(
    "import { getAchievementDefs, getUnlockedAchievements, checkAndUnlockAchievements } from '../service/AchievementService';",
    "import { getAchievementDefs, getUnlockedAchievements, checkAndUnlockAchievements, AchievementDef } from '../service/AchievementService';"
)

# Fix StatItem properties - remove private
text = text.replace(
    '  private label: string = \'\';',
    '  label: string = \'\';'
)
text = text.replace(
    '  private value: string = \'\';',
    '  value: string = \'\';'
)

# Fix StatItem positional args -> named args
text = text.replace(
    "StatItem('总知识点', this.totalKps.toString())",
    "StatItem({ label: '总知识点', value: this.totalKps.toString() })"
)
text = text.replace(
    "StatItem('已完成', this.completedKps.toString())",
    "StatItem({ label: '已完成', value: this.completedKps.toString() })"
)
text = text.replace(
    "StatItem('平均分', this.overallAvgScore + '分')",
    "StatItem({ label: '平均分', value: this.overallAvgScore + '分' })"
)

# Fix ForEach any types
text = text.replace(
    'ForEach(getAchievementDefs(), (def: any) => {',
    'ForEach(getAchievementDefs(), (def: AchievementDef) => {'
)
text = text.replace(
    'ForEach(getUnlockedAchievements(), (ach: any) => {',
    'ForEach(getUnlockedAchievements(), (ach: Achievement) => {'
)

# Add Achievement import
text = text.replace(
    "import { Course } from '../model/DataModel';",
    "import { Course, Achievement } from '../model/DataModel';"
)

# Fix inline userStats object - add type annotation
text = text.replace(
    "const userStats = {\n        lessonsCompleted: completed,\n        perfectScores: 0,\n        knowledgePointsCompleted: completed > 0 ? 1 : 0,\n        streakDays: 1,\n      };",
    "const userStats: Record<string, number> = {\n        'lessonsCompleted': completed,\n        'perfectScores': 0,\n        'knowledgePointsCompleted': completed > 0 ? 1 : 0,\n        'streakDays': 1,\n      };"
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: ProgressDashboardPage.ets')

# ===== 3. ReviewTab - fix any types =====
fp = os.path.join(BASE, 'component', 'ReviewTab.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Change @State reviewsDue: any[] = []; -> define interface locally
# But getReviewsDue returns ReviewDueItem[] (from DatabaseHelper fix), so we need a matching type
if 'interface ReviewDueItem' not in text:
    text = text.replace(
        'export struct ReviewTab {',
        'interface ReviewDueItem {\n  id: number;\n  knowledge_point_id: number;\n  ease_factor: number;\n  interval_days: number;\n  next_review_date: string;\n  review_count: number;\n  avg_score: number;\n  kp_title: string;\n  course_name: string;\n}\n\nexport struct ReviewTab {'
    )
text = text.replace(
    '@State reviewsDue: any[] = [];',
    '@State reviewsDue: ReviewDueItem[] = [];'
)
text = text.replace(
    'ForEach(this.reviewsDue, (item: any) => {',
    'ForEach(this.reviewsDue, (item: ReviewDueItem) => {'
)
text = text.replace(
    '(item: any) => item.id.toString()',
    '(item: ReviewDueItem) => item.id.toString()'
)
text = text.replace(
    'item: any = {};',
    'item: ReviewDueItem = new ReviewDueItem();'
)

# Actually, can't instantiate interfaces. Use object initializer
text = text.replace(
    'item: ReviewDueItem = new ReviewDueItem();',
    'item: ReviewDueItem = { id: 0, knowledge_point_id: 0, ease_factor: 0, interval_days: 0, next_review_date: \'\', review_count: 0, avg_score: 0, kp_title: \'\', course_name: \'\' };'
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: ReviewTab.ets')

# ===== 4. ShareUtil.ets - fix any return type =====
fp = os.path.join(BASE, 'service', 'ShareUtil.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Fix function getPastable(): any
text = text.replace(
    'function getPastable(): any {',
    'function getPastable(): string {'
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: ShareUtil.ets')

# ===== 5. HomePage.ets - verify TabItem onClick not still wrong =====
fp = os.path.join(BASE, 'pages', 'HomePage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
# Check for any remaining positional TabItem calls
if "TabItem('" in text:
    print('WARNING: HomePage.ets still has positional TabItem calls')
else:
    print('OK: HomePage.ets TabItem calls are all named')
if 'onClick' in text and 'TabItem({' in text:
    # Check if the onClick is in our TabItem struct (which uses onPress now)
    if 'onPress' in text and '\n  onPress:' in text:
        print('OK: HomePage.ets TabItem struct uses onPress')
    else:
        print('WARNING: HomePage.ets TabItem might have onClick conflict')

print('\nAll fixes applied.')
