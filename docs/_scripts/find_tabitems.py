"""Find TabItem usage."""
import os

fp = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets\pages\HomePage.ets'
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i, line in enumerate(lines):
    if 'TabItem' in line or 'TabItem' in line:
        print(f'Line {i+1}: {repr(line[:80])}')
