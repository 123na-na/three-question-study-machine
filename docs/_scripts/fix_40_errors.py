"""Fix all 40 compilation errors."""
import os, re

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

# ===== 1. AIService.ets:29 - type the body object =====
fp = os.path.join(BASE, 'service', 'AIService.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text
text = text.replace(
    'const body = { question, user_answer: userAnswer, step };',
    "const body: Record<string, string> = { 'question': question, 'user_answer': userAnswer, 'step': step };"
)
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: AIService.ets:29')

# ===== 2. StatsTab.ets:283 - object literal as type =====
fp = os.path.join(BASE, 'component', 'StatsTab.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text
# Replace inline type with interface + typed default
text = text.replace(
    "  range: { min: number; max: number; label: string; color: string } = { min: 0, max: 0, label: '', color: '' };",
    "  range: MasteryRange = { min: 0, max: 0, label: '', color: '' };"
)
# Add interface before struct
# Move it right before @Component struct MasteryBar
text = text.replace(
    "@Component\n\nstruct MasteryBar",
    "interface MasteryRange {\n  min: number;\n  max: number;\n  label: string;\n  color: string;\n}\n\n@Component\n\nstruct MasteryBar"
)
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: StatsTab.ets:283')

# ===== 3. LearningReportPage.ets:185 - as any =====
fp = os.path.join(BASE, 'pages', 'LearningReportPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text
text = text.replace(
    'const context = getContext(this) as any;',
    'const context = getContext(this);'
)
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: LearningReportPage.ets:185')

# ===== 4. AchievementService.ets:60 - return type + condition prop =====
fp = os.path.join(BASE, 'service', 'AchievementService.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text
# Change getAchievementDefs to return AchievementDef[] but with dummy condition
# OR better: create a separate view interface without condition
text = text.replace(
    "export function getAchievementDefs(): AchievementDef[] {\n  return ACHIEVEMENT_DEFS.map((def) => ({ id: def.id, name: def.name, description: def.description, icon: def.icon }));\n}",
    "export function getAchievementDefs(): AchievementDef[] {\n  return ACHIEVEMENT_DEFS.map((def) => ({ id: def.id, name: def.name, description: def.description, icon: def.icon, condition: def.condition }));\n}"
)
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: AchievementService.ets:60')

# ===== 5. ProgressDashboardPage.ets:89 - userStats =====
fp = os.path.join(BASE, 'pages', 'ProgressDashboardPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text
# Change Record<string, number> back to properly typed object
text = text.replace(
    "const userStats: Record<string, number> = {\n        'lessonsCompleted': completed,\n        'perfectScores': 0,\n        'knowledgePointsCompleted': completed > 0 ? 1 : 0,\n        'streakDays': 1,\n      };",
    "const userStats = {\n        lessonsCompleted: completed,\n        perfectScores: 0,\n        knowledgePointsCompleted: completed > 0 ? 1 : 0,\n        streakDays: 1,\n      } as const;"
)
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: ProgressDashboardPage.ets:89')

# ===== 6. SampleCourseLoader.ets - type arrays and objects =====
fp = os.path.join(BASE, 'service', 'SampleCourseLoader.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Add interfaces before the arrays
text = text.replace(
    "import { getCourseCount, addCourse, addKnowledgePoint } from './DatabaseHelper';",
    "import { getCourseCount, addCourse, addKnowledgePoint } from './DatabaseHelper';\n\ninterface SampleKP {\n  title: string;\n  content: string;\n}\n\ninterface SampleCourse {\n  name: string;\n  description: string;\n  knowledgePoints: SampleKP[];\n}"
)

# Type the SAMPLE_COURSES
text = text.replace(
    "const SAMPLE_COURSES = [",
    "const SAMPLE_COURSES: SampleCourse[] = ["
)

# Type each course object's knowledgePoints array
# The knowledgePoints arrays should be SampleKP[] but they're already typed
# via the interface. The issue is the array literals within need elements of inferrable type.
# Since we typed the outer structure, the inner ones should be inferrable from context.

# Actually the issue is that the elements in the arrays need to be typed.
# In ArkTS, `[{ title: '...', content: '...' }]` in a typed array should be OK if the type is `SampleKP[]`.
# But `{ title: '...', content: '...' }` are object literals. They should be typed by the context.

# Let's try adding `as SampleCourse` to each course entry
# Pattern: Replace each `{` after `SAMPLE_COURSES: SampleCourse[] = [` with typed versions
# This is complex. Let me use a simpler approach: cast each course with `as SampleCourse`

text = text.replace(
    "[\n    {\n      title: '变量与数据类型',",
    "[(\n    {\n      title: '变量与数据类型',"
)

# Hmm, this approach is getting complicated. Let me try a different strategy.
# The real issue is that each array element (course) is an object literal.
# If the array is typed `SampleCourse[]`, each element should be inferrable from the array type.

# Actually, let me revert and try a simpler approach: just type the array elements
# one by one by wrapping each course object in an identity function or cast.

text = orig  # revert

# Add the interfaces
text = text.replace(
    "import { getCourseCount, addCourse, addKnowledgePoint } from './DatabaseHelper';",
    "import { getCourseCount, addCourse, addKnowledgePoint } from './DatabaseHelper';\n\ninterface SampleKP {\n  title: string;\n  content: string;\n}\n\ninterface SampleCourse {\n  name: string;\n  description: string;\n  knowledgePoints: SampleKP[];\n}"
)

# Type the array
text = text.replace(
    "const SAMPLE_COURSES = [",
    "const SAMPLE_COURSES: SampleCourse[] = ["
)

# Now the inner array literals (knowledgePoints) should be inferrable as SampleKP[]
# because the outer array is typed SampleCourse[] which has knowledgePoints: SampleKP[]
# 
# For the object literals inside, they should be typed by context.
# But as a fallback, let me add `as SampleKP` to each knowledge point
text = text.replace(
    "title: '变量与数据类型', content: 'Python 中的变量不需要声明类型，可以直接赋值。常见数据类型包括整数(int)、浮点数(float)、字符串(str)、布尔值(bool)、列表(list)、元组(tuple)、字典(dict)等。'",
    "title: '变量与数据类型', content: 'Python 中的变量不需要声明类型，可以直接赋值。常见数据类型包括整数(int)、浮点数(float)、字符串(str)、布尔值(bool)、列表(list)、元组(tuple)、字典(dict)等。'"
)
# Actually let me just try the simple cast approach for the first course
# SAMPLE_COURSES is now typed, the elements should be inferrable

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: SampleCourseLoader.ets')

# Let me also check if there are remaining issues
with open(fp, 'r', encoding='utf-8') as f:
    final_text = f.read()
    
if 'SampleCourse[]' in final_text:
    print('  SampleCourseLoader type verification: SampleCourse[] found')
    
# ===== 7. HomePage.ets:223,229 - missing closing brace =====
fp = os.path.join(BASE, 'pages', 'HomePage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Fix line 219-223: TabItem multi-line callback needs extra }
# Current:
#   TabItem({ icon: '📊', label: '统计', active: this.selectedTab === 1, onPress: () => {
#     router.pushUrl({ url: 'pages/ProgressDashboardPage' });
#   })
# Should be:
#   TabItem({ icon: '📊', label: '统计', active: this.selectedTab === 1, onPress: () => {
#     router.pushUrl({ url: 'pages/ProgressDashboardPage' });
#   } })
# OR make it single-line

# Make them single-line
text = text.replace(
    "TabItem({ icon: '\U0001f4ca', label: '\u7edf\u8ba1', active: this.selectedTab === 1, onPress: () => {\n\n          router.pushUrl({ url: 'pages/ProgressDashboardPage' });\n\n        })",
    "TabItem({ icon: '\U0001f4ca', label: '\u7edf\u8ba1', active: this.selectedTab === 1, onPress: () => { router.pushUrl({ url: 'pages/ProgressDashboardPage' }); } })"
)
text = text.replace(
    "TabItem({ icon: '\U0001f464', label: '\u6211\u7684', active: this.selectedTab === 2, onPress: () => {\n\n          router.pushUrl({ url: 'pages/LearningReportPage' });\n\n        })",
    "TabItem({ icon: '\U0001f464', label: '\u6211\u7684', active: this.selectedTab === 2, onPress: () => { router.pushUrl({ url: 'pages/LearningReportPage' }); } })"
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: HomePage.ets:223,229')

# ===== 8. ReviewTab.ets:9,23 - interface before @Component =====
fp = os.path.join(BASE, 'component', 'ReviewTab.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Current:
# @Component
#
# interface ReviewDueItem { ... }
#
# export struct ReviewTab {
# 
# Fixed: move interface before @Component
text = text.replace(
    "@Component\n\ninterface ReviewDueItem {\n  id: number;\n  knowledge_point_id: number;\n  ease_factor: number;\n  interval_days: number;\n  next_review_date: string;\n  review_count: number;\n  avg_score: number;\n  kp_title: string;\n  course_name: string;\n}\n\nexport struct ReviewTab {",
    "interface ReviewDueItem {\n  id: number;\n  knowledge_point_id: number;\n  ease_factor: number;\n  interval_days: number;\n  next_review_date: string;\n  review_count: number;\n  avg_score: number;\n  kp_title: string;\n  course_name: string;\n}\n\n@Component\n\nexport struct ReviewTab {"
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: ReviewTab.ets:9,23')

print('\nAll 8 fix categories applied. Build again to verify.')
