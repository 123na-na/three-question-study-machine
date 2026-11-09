"""Check encoding status of corrupted files."""
import os

base = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

fp = os.path.join(base, 'pages', 'LoginPage.ets')
with open(fp, 'rb') as f:
    raw = f.read()

print(f'Total bytes: {len(raw)}')
has_bom = raw[:3] == b'\xef\xbb\xbf'
print(f'Has BOM: {has_bom}')

if has_bom:
    content = raw[3:]
else:
    content = raw

text = content.decode('utf-8')
lines = text.split('\n')

for i in range(60, 85):
    if i < len(lines):
        has_high = any(ord(c) > 127 for c in lines[i])
        if has_high:
            print(f'  Line {i+1}: {lines[i][:80]}')
