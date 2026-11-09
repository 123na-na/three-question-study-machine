"""Fix duplicate import in LearningSessionPage."""
fp = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets\pages\LearningSessionPage.ets'
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove duplicate processReviewResult import
old = "import { processReviewResult } from '../service/SpacedRepetitionService';\n\nimport { processReviewResult } from '../service/SpacedRepetitionService';\n\n"
new = "import { processReviewResult } from '../service/SpacedRepetitionService';\n\n"
if old in text:
    text = text.replace(old, new)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed duplicate import')
else:
    print('Pattern not found, trying alternate...')
    # Try simpler dedup
    lines = text.split('\n')
    seen = set()
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('import ') and stripped in seen:
            continue
        if stripped.startswith('import '):
            seen.add(stripped)
        result.append(line)
    text = '\n'.join(result)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Deduplication complete')
