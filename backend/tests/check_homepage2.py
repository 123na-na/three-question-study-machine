"""Check issues without printing Unicode."""
fp = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets\pages\HomePage.ets'
with open(fp, 'r', encoding='utf-8') as f:
    lines = f.readlines()

count_tab = sum(1 for l in lines if 'TabItem' in l)
count_onclick = sum(1 for l in lines if 'onClick' in l)
count_ontap = sum(1 for l in lines if 'onTap' in l)

print(f'Total lines: {len(lines)}')
print(f'Lines with TabItem: {count_tab}')
print(f'Lines with onClick: {count_onclick}')
print(f'Lines with onTap: {count_ontap}')

# Find first TabItem and onClick lines
for i, line in enumerate(lines):
    stripped = line.strip()
    if 'TabItem' in stripped:
        print(f'TabItem at line {i+1}: {repr(stripped[:60])}')
        break

for i, line in enumerate(lines):
    stripped = line.strip()
    if 'onClick' in stripped:
        print(f'onClick at line {i+1}: {repr(stripped[:60])}')
        break

for i, line in enumerate(lines):
    stripped = line.strip()
    if 'onTap' in stripped:
        print(f'onTap at line {i+1}: {repr(stripped[:60])}')
        break
