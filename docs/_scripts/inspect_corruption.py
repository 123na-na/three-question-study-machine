"""Inspect the encoding corruption in .ets files."""
import os

base = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

# Read AppConstants.ets
fp = os.path.join(base, 'constants', 'AppConstants.ets')
with open(fp, 'rb') as f:
    raw = f.read()

print(f'File size: {len(raw)} bytes')
print(f'Has BOM: {raw[:3] == b"\\xef\\xbb\\xbf"}')

# Strip BOM
if raw[:3] == b'\\xef\\xbb\\xbf':
    raw = raw[3:]

# Decode as UTF-8
try:
    text = raw.decode('utf-8')
    print('UTF-8 decode OK')
except UnicodeDecodeError as e:
    print(f'UTF-8 decode failed: {e}')
    # Find the problematic bytes
    for pos in range(len(raw)):
        try:
            raw[pos:pos+1].decode('utf-8')
        except:
            print(f'Bad byte at position {pos}: {raw[pos]:02x}')
            break

# Print key lines
print('\n--- File content around corrupted areas ---')
lines = text.split('\n')
for i, line in enumerate(lines):
    # Check for any line with non-ASCII characters
    has_non_ascii = any(ord(c) > 127 for c in line)
    if has_non_ascii and ('LABEL' in line or 'level' in line or '权重' in line or 'SCORE' in line):
        print(f'  Line {i+1}: {line}')
