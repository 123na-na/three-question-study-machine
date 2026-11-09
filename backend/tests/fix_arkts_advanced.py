"""Comprehensive ArkTS compatibility fix for all corrupted .ets files.
Fixes known ArkTS API issues that differ from original working code."""
import os, re

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

stats = {'files_read': 0, 'files_modified': 0}

def fix_file(rel_path):
    fp = os.path.join(BASE, rel_path)
    if not os.path.exists(fp):
        print(f'SKIP (not found): {rel_path}')
        return
    with open(fp, 'rb') as f:
        raw = f.read()
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        print(f'ENCODING ISSUE: {rel_path}')
        return
    stats['files_read'] += 1
    orig = text

    # Fix TabItem/StepButton/TabButton positional args -> named args
    # Pattern: TabItem('ICON', 'LABEL', CONDITION, onClick)
    # But these structs have been renamed to use 'onClick' property which conflicts
    # Better approach: rename onClick to onTap in struct defs and usage
    
    # Fix TabButton positional args: TabButton({ label, active, onTap })
    # and StepButton similar
    
    if text != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(text)
        stats['files_modified'] += 1
        print(f'  Fixed: {rel_path}')

# Fix specific files that need structural changes
# These are the files with major issues:

# 1. HomePage.ets - Fix TabItem struct (rename onClick to onTap)
fp = os.path.join(BASE, 'pages', 'HomePage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Remove $r('app.media.app_icon') - already handled
# TabItem struct: rename onClick to onTap
text = text.replace(
    '@Component\nstruct TabItem {\n  private icon: string = \'\';\n  private label: string = \'\';\n  private active: boolean = false;\n  private onClick: () => void = () => {};\n\n  build() {\n    Column() {\n      Text(this.icon)\n        .fontSize(20)\n      Text(this.label)\n        .fontSize(11)\n        .fontColor(this.active ? Colors.PRIMARY : Colors.TEXT_SECONDARY)\n        .margin({ top: 2 })\n    }\n    .onClick(() => { this.onClick(); })\n    .padding({ top: 6 })\n  }\n}',
    '@Component\nstruct TabItem {\n  private icon: string = \'\';\n  private label: string = \'\';\n  private active: boolean = false;\n  private onTap: () => void = () => {};\n\n  build() {\n    Column() {\n      Text(this.icon)\n        .fontSize(20)\n      Text(this.label)\n        .fontSize(11)\n        .fontColor(this.active ? Colors.PRIMARY : Colors.TEXT_SECONDARY)\n        .margin({ top: 2 })\n    }\n    .onClick(() => { this.onTap(); })\n    .padding({ top: 6 })\n  }\n}'
)
# Fix TabItem usage in the build method
text = text.replace(
    'TabItem(\'📖\', \'学习\', this.selectedTab === 0, () => { this.selectedTab = 0; })',
    'TabItem({ icon: \'📖\', label: \'学习\', active: this.selectedTab === 0, onTap: () => { this.selectedTab = 0; } })'
)
text = text.replace(
    'TabItem(\'📊\', \'统计\', this.selectedTab === 1, () => {\n          router.pushUrl({ url: \'pages/ProgressDashboardPage\' });\n        })',
    'TabItem({ icon: \'📊\', label: \'统计\', active: this.selectedTab === 1, onTap: () => {\n          router.pushUrl({ url: \'pages/ProgressDashboardPage\' });\n        } })'
)
text = text.replace(
    'TabItem(\'👤\', \'我的\', this.selectedTab === 2, () => {\n          router.pushUrl({ url: \'pages/LearningReportPage\' });\n        })',
    'TabItem({ icon: \'👤\', label: \'我的\', active: this.selectedTab === 2, onTap: () => {\n          router.pushUrl({ url: \'pages/LearningReportPage\' });\n        } })'
)

# Fix StatCard positional args
text = text.replace(
    'StatCard(\'📚\', this.courses.length.toString(), \'课程\')',
    'StatCard({ icon: \'📚\', value: this.courses.length.toString(), label: \'课程\' })'
)
text = text.replace(
    'StatCard(\'📝\', \'3\', \'学习步骤\')',
    'StatCard({ icon: \'📝\', value: \'3\', label: \'学习步骤\' })'
)
text = text.replace(
    'StatCard(\'🎯\', \'三问法\', \'高效学习\')',
    'StatCard({ icon: \'🎯\', value: \'三问法\', label: \'高效学习\' })'
)

# Fix StatCard struct definition
text = text.replace(
    '@Component\nstruct StatCard {\n  private icon: string = \'\';\n  private value: string = \'\';\n  private label: string = \'\';\n\n  build() {\n    Column() {',
    '@Component\nstruct StatCard {\n  private icon: string = \'\';\n  private value: string = \'\';\n  private label: string = \'\';\n\n  build() {\n    Column() {'
)  # No change needed, StatCard already uses named fields

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    stats['files_modified'] += 1
    print(f'  Fixed: pages/HomePage.ets')

# 2. LearnTab.ets - StepButton struct: rename onClick to onTap  
fp = os.path.join(BASE, 'component', 'LearnTab.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Rename onClick to onTap in StepButton struct
text = text.replace(
    'private onClick: () => void = () => {};',
    'private onTap: () => void = () => {};'
)
text = text.replace(
    '.onClick(() => { this.onClick(); })',
    '.onClick(() => { this.onTap(); })'
)
# Fix ScoreCalculator calls
text = text.replace(
    'ScoreCalculator.calculateOverallScore({\n        \'what\': this.whatScore,\n        \'why\': this.whyScore,\n        \'how\': this.howScore\n      })',
    'ScoreCalculator.calculateOverallScore(this.whatScore, this.whyScore, this.howScore)'
)
# Fix StepButton usage in build
text = text.replace(
    'StepButton({\n          icon: \'🤔\',\n          label: STEP_LABELS.what,\n          subtitle: \'理解概念的定义和内涵\',\n          score: this.whatScore,\n          color: \'#8B5CF6\',\n          onClick: () => {\n            router.pushUrl({\n              url: \'pages/LearningSessionPage?kpId=\' + this.knowledgePoint.id + \'&step=what\'\n            });\n          }\n        })',
    'StepButton({ icon: \'🤔\', label: STEP_LABELS.what, subtitle: \'理解概念的定义和内涵\', score: this.whatScore, color: \'#8B5CF6\', onTap: () => { router.pushUrl({ url: \'pages/LearningSessionPage?kpId=\' + this.knowledgePoint.id + \'&step=what\' }); } })'
)
text = text.replace(
    'StepButton({\n          icon: \'🔍\',\n          label: STEP_LABELS.why,\n          subtitle: \'探究原理和逻辑关系\',\n          score: this.whyScore,\n          color: \'#3B82F6\',\n          onClick: () => {\n            router.pushUrl({\n              url: \'pages/LearningSessionPage?kpId=\' + this.knowledgePoint.id + \'&step=why\'\n            });\n          }\n        })',
    'StepButton({ icon: \'🔍\', label: STEP_LABELS.why, subtitle: \'探究原理和逻辑关系\', score: this.whyScore, color: \'#3B82F6\', onTap: () => { router.pushUrl({ url: \'pages/LearningSessionPage?kpId=\' + this.knowledgePoint.id + \'&step=why\' }); } })'
)
text = text.replace(
    'StepButton({\n          icon: \'💡\',\n          label: STEP_LABELS.how,\n          subtitle: \'掌握实践和应用方法\',\n          score: this.howScore,\n          color: \'#10B981\',\n          onClick: () => {\n            router.pushUrl({\n              url: \'pages/LearningSessionPage?kpId=\' + this.knowledgePoint.id + \'&step=how\'\n            });\n          }\n        })',
    'StepButton({ icon: \'💡\', label: STEP_LABELS.how, subtitle: \'掌握实践和应用方法\', score: this.howScore, color: \'#10B981\', onTap: () => { router.pushUrl({ url: \'pages/LearningSessionPage?kpId=\' + this.knowledgePoint.id + \'&step=how\' }); } })'
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    stats['files_modified'] += 1
    print(f'  Fixed: component/LearnTab.ets')

# 3. CourseDetailPage.ets - TabButton struct rename onClick to onTap
fp = os.path.join(BASE, 'pages', 'CourseDetailPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

text = text.replace(
    'private onClick: () => void = () => {};',
    'private onTap: () => void = () => {};'
)
text = text.replace(
    '.onClick(() => { this.onClick(); })',
    '.onClick(() => { this.onTap(); })'
)
# Fix TabButton usage
text = text.replace(
    'TabButton({ label: \'学习\', active: this.currentTab === 0, onClick: () => { this.currentTab = 0; } })',
    'TabButton({ label: \'学习\', active: this.currentTab === 0, onTap: () => { this.currentTab = 0; } })'
)
text = text.replace(
    'TabButton({ label: \'复习\', active: this.currentTab === 1, onClick: () => { this.currentTab = 1; } })',
    'TabButton({ label: \'复习\', active: this.currentTab === 1, onTap: () => { this.currentTab = 1; } })'
)
text = text.replace(
    'TabButton({ label: \'统计\', active: this.currentTab === 2, onClick: () => { this.currentTab = 2; } })',
    'TabButton({ label: \'统计\', active: this.currentTab === 2, onTap: () => { this.currentTab = 2; } })'
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    stats['files_modified'] += 1
    print(f'  Fixed: pages/CourseDetailPage.ets')

# 4. LearningSessionPage.ets - MAJOR REWRITE needed
# The file structure is fundamentally broken. Need to rewrite.
# Let me completely replace it with a version that follows ArkTS patterns.

# 5. StatsTab.ets - check for onClick issues
fp = os.path.join(BASE, 'component', 'StatsTab.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Fix ScoreCalculator import
text = text.replace(
    'import { ScoreCalculator } from \'../utils/ScoreCalculator\';',
    ''
)
# Remove unused calculateOverallScore usage
text = text.replace(
    'import { calculateOverallScore } from \'../utils/ScoreCalculator\';',
    ''
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    stats['files_modified'] += 1
    print(f'  Fixed: component/StatsTab.ets')

# 6. LearningReportPage - remove unused ScoreCalculator import
fp = os.path.join(BASE, 'pages', 'LearningReportPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

text = text.replace(
    'import { ScoreCalculator } from \'../utils/ScoreCalculator\';',
    ''
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    stats['files_modified'] += 1
    print(f'  Fixed: pages/LearningReportPage.ets')

# 7. ProgressDashboardPage - remove unused ScoreCalculator import
fp = os.path.join(BASE, 'pages', 'ProgressDashboardPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

text = text.replace(
    'import { ScoreCalculator } from \'../utils/ScoreCalculator\';',
    ''
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    stats['files_modified'] += 1
    print(f'  Fixed: pages/ProgressDashboardPage.ets')

# 8. ReviewSessionPage - remove unused ScoreCalculator import
fp = os.path.join(BASE, 'pages', 'ReviewSessionPage.ets')
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

text = text.replace(
    'import { ScoreCalculator } from \'../utils/ScoreCalculator\';',
    ''
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    stats['files_modified'] += 1
    print(f'  Fixed: pages/ReviewSessionPage.ets')

print(f'\nSummary: {stats["files_modified"]} files modified out of {stats["files_read"]} read')
