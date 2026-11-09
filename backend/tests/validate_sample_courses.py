"""Validate all sample course JSON files."""
import json
import os
import glob

base = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\resources\rawfile\sample_courses'
files = glob.glob(os.path.join(base, '*.json'))
print(f'Found {len(files)} sample course files:')
all_ok = True
for f in sorted(files):
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    kp_count = len(data.get('knowledge_points', []))
    # Verify each KP has title and content
    for i, kp in enumerate(data.get('knowledge_points', [])):
        if not kp.get('title') or not kp.get('content'):
            print(f'  ERROR: {os.path.basename(f)} KP #{i} missing title or content')
            all_ok = False
    status = 'OK' if all_ok else 'INVALID'
    print(f'  {os.path.basename(f)}: "{data["name"]}" ({kp_count} KPs)')

if all_ok:
    print('All sample courses valid!')
else:
    print('SOME COURSES HAVE ERRORS!')
