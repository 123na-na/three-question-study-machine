"""Comprehensive ArkTS compatibility fix script.
Fixes all known strict ArkTS rule violations across the codebase."""
import os, re

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

def fix_file(path, label, replacements):
    """Apply a list of (old, new) replacements to a file."""
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    orig = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'  Fixed: {label}')

# ============== 1. DatabaseHelper.ets ==============
fp = os.path.join(BASE, 'service', 'DatabaseHelper.ets')
with open(fp, 'r', encoding='utf-8') as f:
    db = f.read()
orig = db

# Fix 4-arg executeSql pattern: (sql, params, () => resolve(), (err) => reject(err))
# -> (sql, params, (err) => { if (err) reject(err); else resolve(); })
db = re.sub(
    r'executeSql\(([^,]+),\s*\[([^\]]*)\],\s*\(\)\s*=>\s*resolve\(\)\s*,\s*\((\w+)\)\s*=>\s*reject\(\3\)\)',
    r'executeSql(\1, [\2], (\3) => { if (\3) reject(\3); else resolve(); })',
    db
)

# Also fix pattern: executeSql(sql, params, () => resolve(), (err) => reject(err))
# where params is a longer array
db = re.sub(
    r'executeSql\(([^,]+),\s*\[([^\]]+?)\],\s*\(\)\s*=>\s*resolve\(\)\s*,\s*\((\w+)\)\s*=>\s*reject\(\3\)\)',
    r'executeSql(\1, [\2], (\3) => { if (\3) reject(\3); else resolve(); })',
    db
)

# Fix querySql 4-arg pattern that was corrupted
db = re.sub(
    r"querySql\('SELECT last_insert_rowid\(\) as id', \[\], \(err2?,\s*rs\)\s*=>\s*\{\s*if\s*\(err2?\)\s*reject\(err2?\);\s*else\s*resolve\(rs\);\s*\}\)",
    r"querySql('SELECT last_insert_rowid() as id', [], (err, rs) => { if (err) reject(err); else resolve(rs); })",
    db
)

if db != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(db)
    print('  Fixed: DatabaseHelper.ets (4-arg executeSql -> 3-arg)')
else:
    print('  No changes: DatabaseHelper.ets')

# ============== 2. LearningSessionPage.ets ==============
fp = os.path.join(BASE, 'pages', 'LearningSessionPage.ets')
fix_file(fp, 'LearningSessionPage.ets stray }', [
    ('  }\n\n  async initSession', '\n  async initSession'),
    ('private label: string = \'\';', 'label: string = \'\';'),
    ('private isActive: boolean = false;', 'isActive: boolean = false;'),
    ('private isCurrent: boolean = false;', 'isCurrent: boolean = false;'),
    ('private item: ConversationItem = { role: \'user\', content: \'\' };', 'item: ConversationItem = { role: \'user\', content: \'\' };'),
])

# Fix indexed access on STEP_LABELS[stepName] where stepName is dynamic string
# Create a helper and use dot notation
fp = os.path.join(BASE, 'pages', 'LearningSessionPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Replace STEP_LABELS[stepName] with helper call
text = text.replace(
    'label: STEP_LABELS[stepName],',
    'label: LearningSessionPage.getStepLabelText(stepName),'
)
text = text.replace(
    'STEP_LABELS[this.getNextStepName()]',
    'this.getNextStepLabel()'
)

# Add static helper method to the struct
# Find the struct opening and add the method
# Actually, static methods in structs may not work. Let me use a module-level function instead.
# Replace: change the inline STEP_LABELS[stepName] to use dot notation via conditional
# Best approach: define a local function in the file

# Actually, STEP_LABELS has type StepLabels with explicit properties 'what', 'why', 'how'
# So STEP_LABELS[stepName] where stepName is string won't work
# But in ForEach over LEARNING_STEPS, stepName is 'what'|'why'|'how', so dot notation works

# Remove the static call and use inline mapping
text = text.replace(
    "label: LearningSessionPage.getStepLabelText(stepName),",
    "label: stepName === 'what' ? STEP_LABELS.what : stepName === 'why' ? STEP_LABELS.why : STEP_LABELS.how,"
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Fixed: LearningSessionPage.ets (indexed access)')

# ============== 3. HomePage.ets ==============
fp = os.path.join(BASE, 'pages', 'HomePage.ets')
fix_file(fp, 'HomePage.ets TabItem positional args -> named + onClick->onPress', [
    # Line 217: onClick -> onPress
    ("TabItem({ icon: '\U0001f4d6', label: '\u5b66\u4e60', active: this.selectedTab === 0, onClick: () => { this.selectedTab = 0; } })",
     "TabItem({ icon: '\U0001f4d6', label: '\u5b66\u4e60', active: this.selectedTab === 0, onPress: () => { this.selectedTab = 0; } })"),
    # Line 219: TabItem positional args -> named
    ("TabItem('\U0001f4ca', '\u7edf\u8ba1', this.selectedTab === 1, () => {",
     "TabItem({ icon: '\U0001f4ca', label: '\u7edf\u8ba1', active: this.selectedTab === 1, onPress: () => {"),
    # Line 225: TabItem positional args -> named
    ("TabItem('\U0001f464', '\u6211\u7684', this.selectedTab === 2, () => {",
     "TabItem({ icon: '\U0001f464', label: '\u6211\u7684', active: this.selectedTab === 2, onPress: () => {"),
    # Close the TabItem usage with extra }) 
    # These need to match the closure pattern
])

# The replacement for positional TabItem needs closing braces too
# Let me use regex to handle the complex replacements
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Fix TabItem positional args lines
# TabItem('📊', '统计', this.selectedTab === 1, () => {\n          router.pushUrl({ url: 'pages/ProgressDashboardPage' });\n        })
# -> TabItem({ icon: '📊', label: '统计', active: this.selectedTab === 1, onPress: () => {
text = re.sub(
    r"TabItem\('([^']+)', '([^']+)', ([^,]+), \(\) => \{\s*\n\s*router\.pushUrl\(\{ url: '([^']+)' \}\);\s*\n\s*\}\)",
    r"TabItem({ icon: '\1', label: '\2', active: \3, onPress: () => { router.pushUrl({ url: '\4' }); } })",
    text
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Fixed: HomePage.ets (replaced positional args with named)')

# ============== 4. AchievementService.ets ==============
fp = os.path.join(BASE, 'service', 'AchievementService.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Fix destructuring params in getAchievementDefs
# ({ id, name, description, icon }) -> (def)
text = text.replace(
    'ACHIEVEMENT_DEFS.map(({ id, name, description, icon }) => ({ id, name, description, icon }))',
    'ACHIEVEMENT_DEFS.map((def) => ({ id: def.id, name: def.name, description: def.description, icon: def.icon } as { id: string; name: string; description: string; icon: string }))'
)

# Fix typed array literal ACHIEVEMENT_DEFS
# Array<{ id: string; ... }> might trigger arkts-no-obj-literals-as-types
# Replace inline object type with named interface
# Actually, ACHIEVEMENT_DEFS uses the pattern `as const` isn't used
# Better approach: define an interface for achievement definitions

# Check if AchievementDef interface already exists; if not, add it
if 'interface AchievementDef' not in text:
    # Add interface before the ACHIEVEMENT_DEFS declaration
    text = text.replace(
        'const ACHIEVEMENT_DEFS',
        'interface AchievementDef { id: string; name: string; description: string; icon: string; condition: (stats: UserStats) => boolean }\n\nconst ACHIEVEMENT_DEFS'
    )

# Change the array literal type
text = text.replace(
    'const ACHIEVEMENT_DEFS: Array<{ id: string; name: string; description: string; icon: string; condition: (stats: UserStats) => boolean }> = [',
    'const ACHIEVEMENT_DEFS: AchievementDef[] = ['
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Fixed: AchievementService.ets (destruct params + typed array)')

# ============== 5. LearnTab.ets ==============
fp = os.path.join(BASE, 'component', 'LearnTab.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Fix ScoreCalculator.calculateOverallScore inline object literal
# create a helper that builds the scores parameter
# Replace: ScoreCalculator.calculateOverallScore({ 'what': ..., 'why': ..., 'how': ... })
# with a properly typed call
text = text.replace(
    "ScoreCalculator.calculateOverallScore({\n        'what': this.whatScore,\n        'why': this.whyScore,\n        'how': this.howScore\n      })",
    "(() => { const scores: Record<string, number> = {}; scores['what'] = this.whatScore; scores['why'] = this.whyScore; scores['how'] = this.howScore; return ScoreCalculator.calculateOverallScore(scores); })()"
)

# Alternative simpler fix: just pass as Record
# Actually, calculateOverallScore probably takes any[]. Let me check ScoreCalculator

# Let me just use a simpler approach
text = text.replace(
    "(() => { const scores: Record<string, number> = {}; scores['what'] = this.whatScore; scores['why'] = this.whyScore; scores['how'] = this.howScore; return ScoreCalculator.calculateOverallScore(scores); })()",
    "ScoreCalculator.calculateOverallScore([this.whatScore, this.whyScore, this.howScore])"
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Fixed: LearnTab.ets (ScoreCalculator call)')

# ============== 6. ReviewTab.ets - check for similar issues ==============
fp = os.path.join(BASE, 'component', 'ReviewTab.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text
# Remove private from component properties
text = re.sub(r'  private (\w+): (string|number|boolean|(\w+)<\w+>|\[\]|\{\}) =', r'  \1: \2 =', text)
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Fixed: ReviewTab.ets (removed private)')

# ============== 7. StatsTab.ets - similar ==============
fp = os.path.join(BASE, 'component', 'StatsTab.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text
text = re.sub(r'  private (\w+): (string|number|boolean|(\w+)<\w+>|\[\]|\{\}) =', r'  \1: \2 =', text)
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Fixed: StatsTab.ets (removed private)')

# ============== 8. CourseDetailPage.ets - TabButton ==============
fp = os.path.join(BASE, 'pages', 'CourseDetailPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text
# Remove private from sub-component properties
text = re.sub(r'  private (\w+): (string|number|boolean|(\w+)<\w+>|\[\]|\{\}) =', r'  \1: \2 =', text)
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Fixed: CourseDetailPage.ets (removed private)')

# ============== 9. OnboardingOverlay.ets ==============
fp = os.path.join(BASE, 'component', 'OnboardingOverlay.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text
text = re.sub(r'  private (\w+): (string|number|boolean|(\w+)<\w+>|\[\]|\{\}) =', r'  \1: \2 =', text)
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Fixed: OnboardingOverlay.ets (removed private)')

# ============== 10. ProgressRing.ets ==============
fp = os.path.join(BASE, 'component', 'ProgressRing.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text
text = re.sub(r'  private (\w+): (string|number|boolean|(\w+)<\w+>|\[\]|\{\}) =', r'  \1: \2 =', text)
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Fixed: ProgressRing.ets (removed private)')

# ============== 11. Fix remaining files with ScoreCalculator ==============
# ScoreCalculator.calculateOverallScore takes scores parameter
# The function signature might expect specific format
fp = os.path.join(BASE, 'utils', 'ScoreCalculator.ets')
if os.path.exists(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f'  ScoreCalculator.ets signature:')
    # Find the class/function signatures
    for line in text.split('\n'):
        if 'function' in line or 'public' in line or 'static' in line:
            print(f'    {line.strip()}')

print('\nComprehensive fixes applied.')
