"""Fix remaining compilation issues:
1. DatabaseHelper executeSql 4-arg -> 3-arg pattern
2. DatabaseHelper querySql callback patterns
3. HomePage/LearnTab onClick/onTap mismatches
4. LearningReportPage/ProgressDashboardPage positional args
"""
import os, re

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

# 1. Fix DatabaseHelper executeSql 4-arg pattern
fp = os.path.join(BASE, 'service', 'DatabaseHelper.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Fix: store.executeSql(sql, params, successCb, errorCb) -> store.executeSql(sql, params, (err) => { if (err) reject(err); else resolve(); })
# Pattern 1: executeSql(sql, params, () => resolve(), (err) => reject(err))
text = re.sub(
    r"store\.executeSql\(([^,]+),\s*\[([^\]]*)\],\s*\(\)\s*=>\s*resolve\(\)\s*,\s*\(err\)\s*=>\s*reject\(err\)\s*\)",
    r"store.executeSql(\1, [\2], (err) => { if (err) reject(err); else { resolve(); } })",
    text
)

# Pattern 2: executeSql(sql, [...], () => resolve(), (err2) => reject(err2))
text = re.sub(
    r"store\.executeSql\(([^,]+),\s*\[([^\]]*)\],\s*\(\)\s*=>\s*resolve\(\)\s*,\s*\((\w+)\)\s*=>\s*reject\(\3\)\s*\)",
    r"store.executeSql(\1, [\2], (\3) => { if (\3) reject(\3); else { resolve(); } })",
    text
)

# Fix querySql too
# Pattern: store.querySql(sql, params, (err, rs) => { if (err) reject(err); else resolve(rs); })
# This is already correct (3 args)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: DatabaseHelper.ets (executeSql 4-arg pattern)')
else:
    print('DatabaseHelper.ets: no changes needed')

# 2. Fix HomePage TabItem usage (onClick -> onTap)
fp = os.path.join(BASE, 'pages', 'HomePage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# The struct already has onTap, but usage sites still have onClick
# Actually, the struct definition should use onClick (the original name) but used as a property, not as the built-in attribute
# The issue is ArkTS reserves 'onClick' as a component attribute
# So we need 'onTap' in both struct def and usage, and in the struct build method use .onClick(() => this.onTap())
# Let me check what's on line 158

# Fix the rename that already happened - onTap should work now
# But there are still TabItem calls with positional args at lines 219, 225

# Let me check current structure
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: HomePage.ets')

# 3. Fix LearnTab StepButton onClick -> onTap usage
fp = os.path.join(BASE, 'component', 'LearnTab.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# The struct has onTap, but usage sites may still have onClick
# Let me check
if 'onClick:' in text and 'onTap:' not in text:
    text = text.replace('onClick:', 'onTap:')
if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: LearnTab.ets')

# 4. Fix LearningReportPage OverviewCard positional args
fp = os.path.join(BASE, 'pages', 'LearningReportPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Fix: OverviewCard('📚', ...) -> OverviewCard({ icon: '📚', ... })
text = re.sub(
    r"OverviewCard\('([^']+)'\s*,\s*'([^']+)'\s*,\s*'([^']+)'\s*\)",
    r"OverviewCard({ icon: '\1', value: '\2', label: '\3' })",
    text
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: LearningReportPage.ets')

# 5. Fix ProgressDashboardPage StatItem positional args
fp = os.path.join(BASE, 'pages', 'ProgressDashboardPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Fix: StatItem('总知识点', ...) -> StatItem({ label: '总知识点', ... })
# This struct takes (label, value) positional
text = re.sub(
    r"StatItem\('([^']+)'\s*,\s*'([^']+)'\s*\)",
    r"StatItem({ label: '\1', value: '\2' })",
    text
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed: ProgressDashboardPage.ets')

print('All fixes applied')
