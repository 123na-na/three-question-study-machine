"""Check TabItem and TabButton issues."""
fp = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets\pages\HomePage.ets'
with open(fp, 'r', encoding='utf-8') as f:
    lines = f.readlines()

found = False
for i, line in enumerate(lines):
    stripped = line.strip()
    if 'TabItem' in stripped or 'onClick' in stripped:
        print(f'{i+1}: {stripped[:80]}')
        found = True
if not found:
    print('No TabItem or onClick found')

print(f'\nTotal lines: {len(lines)}')
print(f'Lines with TabItem: {sum(1 for l in lines if "TabItem" in l)}')
print(f'Lines with onClick: {sum(1 for l in lines if "onClick" in l)}')
