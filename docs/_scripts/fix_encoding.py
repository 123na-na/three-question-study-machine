"""
Fix UTF-8 encoding corruption in .ets files.
The corruption happened because PowerShell read UTF-8 files as system default encoding (GBK on Chinese Windows)
then wrote them back as UTF-8 with BOM.
"""
import os
import glob

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

def fix_file(filepath):
    """Attempt to fix encoding corruption by trying various round-trips."""
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    # Strip BOM if present
    if raw[:3] == b'\xef\xbb\xbf':
        raw = raw[3:]
    
    # Try to decode as UTF-8 first
    try:
        text = raw.decode('utf-8')
        # Check if text looks correct (has proper Chinese)
        has_proper_chinese = False
        for ch in ['三', '问', '学', '习', '机', '是', '什', '么', '为', '怎', '用']:
            if ch in text:
                has_proper_chinese = True
                break
        if has_proper_chinese:
            # Text seems OK, just write back without BOM
            with open(filepath, 'wb') as f:
                f.write(raw)
            return 'ok'
    except:
        pass
    
    # Try the common corruption patterns
    # Pattern 1: UTF-8 read as GBK, then written as UTF-8
    try:
        # Current content is UTF-8 garbled from GBK misread
        # Step 1: Read currently as UTF-8
        text = raw.decode('utf-8')
        
        # Step 2: Try to encode each character and see if it forms valid UTF-8
        # The corruption: original UTF-8 bytes were interpreted as GBK
        # So text[j] in current file = the character whose GBK encoding equals original UTF-8 bytes
        
        # Fix: for each character, try GBK encoding, then check if result is valid UTF-8
        # Actually, try: re-encode the garbled text back through the same pipeline
        
        # Common fix: encode garbled text as latin-1, then decode as utf-8
        try:
            fixed = text.encode('latin-1').decode('utf-8')
            # Check if it has proper Chinese
            if '三' in fixed or '是' in fixed:
                with open(filepath, 'wb') as f:
                    f.write(fixed.encode('utf-8'))
                return 'fixed-latin1'
        except:
            pass
        
        # Try GBK round-trip
        try:
            fixed = text.encode('gbk').decode('utf-8')
            if '三' in fixed or '是' in fixed:
                with open(filepath, 'wb') as f:
                    f.write(fixed.encode('utf-8'))
                return 'fixed-gbk'
        except:
            pass
            
    except Exception as e:
        return f'error: {e}'
    
    return 'unfixable'

# Find all ets files
all_files = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f.endswith('.ets'):
            all_files.append(os.path.join(root, f))

print(f'Found {len(all_files)} .ets files')

results = {}
for fp in sorted(all_files):
    rel = os.path.relpath(fp, BASE)
    result = fix_file(fp)
    results[rel] = result
    print(f'  {result:15s} {rel}')

ok = sum(1 for v in results.values() if v == 'ok')
fixed = sum(1 for v in results.values() if v.startswith('fixed'))
failed = sum(1 for v in results.values() if v == 'unfixable' or v.startswith('error'))
print(f'\nOK: {ok}, Fixed: {fixed}, Failed: {failed}')
