"""Replace all router imports and fix common ArkTS issues across all .ets files."""
import os, re

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

changes = 0

# Fix router import: import { router } from '@ohos.router' -> import router from '@ohos.router'
# Also fix import { router, useNavigate } pattern
for root, dirs, files in os.walk(BASE):
    for f in files:
        if not f.endswith('.ets'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'rb') as fh:
            raw = fh.read()
        try:
            orig = raw.decode('utf-8')
        except:
            continue
        
        text = orig
        
        # Fix 1: import { router, useNavigate } from '@ohos.router' -> import router from '@ohos.router'
        text = re.sub(
            r"""import\s*\{\s*router\s*,\s*useNavigate\s*\}\s*from\s*['"]@ohos\.router['"]""",
            "import router from '@ohos.router'",
            text
        )
        
        # Fix 2: import { router } from '@ohos.router' -> import router from '@ohos.router' (only if standalone)
        text = re.sub(
            r"""import\s*\{\s*router\s*\}\s*from\s*['"]@ohos\.router['"]""",
            "import router from '@ohos.router'",
            text
        )
        
        # Fix 3: FontWeight.Semibold -> FontWeight.Medium
        text = text.replace('FontWeight.Semibold', 'FontWeight.Medium')
        
        # Fix 4: 'Semibold' in strings -> 'Medium'
        text = text.replace("'Semibold'", "'Medium'")
        
        # Fix 5: ScoresCalculator import as function -> use class
        # Change: import { calculateOverallScore } from '../utils/ScoreCalculator'
        # To: import { ScoreCalculator } from '../utils/ScoreCalculator'
        text = re.sub(
            r"""import\s*\{\s*calculateOverallScore\s*\}\s*from\s*['"]\.\.\/utils\/ScoreCalculator['"]""",
            "import { ScoreCalculator } from '../utils/ScoreCalculator'",
            text
        )
        
        # Fix 6: calculateOverallScore call -> ScoreCalculator.calculateOverallScore
        # This is trickier - only replace when called as a function
        text = re.sub(
            r"""calculateOverallScore\(\s*\{""",
            "ScoreCalculator.calculateOverallScore({",
            text
        )
        # Also fix the three-arg version used in ProfileTab
        text = re.sub(
            r'(?<!ScoreCalculator\.)calculateOverallScore\((\s*\w+\.score\s*)\)',
            r'ScoreCalculator.calculateOverallScore(\1)',
            text
        )
        
        # Fix 7: onClick with wrong signature in sub-components
        # Change @Link onClick: () => void = () => {} to proper pattern
        # This is harder to fix with regex. Let me handle it file by file.
        
        # Fix 8: Curve.FadeIn -> Curve.Linear or remove animation
        text = text.replace('Curve.FadeIn', 'Curve.Linear')
        
        # Fix 9: maxWidth -> constraintWidth
        text = text.replace('.maxWidth(', '.constraintWidth(')
        
        # Fix 10: animation({ duration: ..., curve: Curve.Linear }) -> remove animation 
        # as ArkTS may not support it in all contexts
        # Let's just remove .animation(...) calls that cause issues
        # text = re.sub(r'\.animation\(\{[^}]*\}\)', '', text)
        # Actually, let's keep them and see if they compile
        
        if text != orig:
            with open(fp, 'w', encoding='utf-8') as fh:
                fh.write(text)
            print(f'Fixed: {os.path.relpath(fp, BASE)}')
            changes += 1

if changes == 0:
    print('No changes needed')
else:
    print(f'\nFixed {changes} files')
