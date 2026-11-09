"""Check utils file corruption."""
import os

base = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

for fn in ['utils/ScoreCalculator.ets', 'utils/ShareUtil.ets']:
    fp = os.path.join(base, fn)
    with open(fp, 'rb') as f:
        raw = f.read()
    if raw[:3] == b'\xef\xbb\xbf':
        raw = raw[3:]
    text = raw.decode('utf-8')
    lines = text.split('\n')
    print(f'=== {fn} ({len(lines)} lines) ===')
    for line in lines[:5]:
        print(f'  {line}')
    
    has_pua = any('\ue000' <= c <= '\uf8ff' for c in text)
    has_repl = '\ufffd' in text
    print(f'  Has private use: {has_pua}, Has replacement: {has_repl}')
    print()
