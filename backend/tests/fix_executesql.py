"""Fix remaining 4-arg executeSql patterns in DatabaseHelper.ets"""
import re

fp = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets\service\DatabaseHelper.ets'
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# Find ALL executeSql calls and fix 4-arg patterns
# Pattern: executeSql(SQL, PARAMS, () => resolve(), (err) => reject(err))
# The SQL and PARAMS can span multiple lines with varying whitespace

# Strategy: match executeSql(, then everything up to (), then the callback pair
# Replace: , (err) => reject(err));  with  , (err) => { if (err) reject(err); else resolve(); });

# Simple text replacement for the exact callback pattern
old_callback = '), () => resolve(), (err) => reject(err)'
new_callback = '), (err) => { if (err) reject(err); else resolve(); }'

count = text.count(old_callback)
if count > 0:
    text = text.replace(old_callback, new_callback)
    print(f'Fixed {count} callback patterns')

# Also fix some cases where the last closing parenthesis is on a different line
old_callback2 = '), () => resolve(), (err) => reject(err)\n  });'
new_callback2 = '), (err) => { if (err) reject(err); else resolve(); }\n  });'
count2 = text.count(old_callback2)
if count2 > 0:
    text = text.replace(old_callback2, new_callback2)
    print(f'Fixed {count2} multi-line callback patterns')

# Also check if some have `, () => resolve(), (err) => reject(err));` (with spaces)
text = re.sub(
    r',\s*\(\s*\)\s*=>\s*resolve\(\)\s*,\s*\(\s*(\w+)\s*\)\s*=>\s*reject\(\1\)\s*\)',
    r', (\1) => { if (\1) reject(\1); else resolve(); })',
    text
)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('DatabaseHelper.ets updated successfully')
else:
    print('No changes needed or pattern mismatch')

# Verify - count executeSql calls and check remaining issues
with open(fp, 'r', encoding='utf-8') as f:
    updated = f.read()

# Count executeSql occurrences
calls = re.findall(r'store\.executeSql\(', updated)
print(f'\nTotal executeSql calls: {len(calls)}')

# Check for remaining 4-arg patterns
remaining = re.search(r'executeSql\([^)]+\(\)\s*=>\s*resolve\(\)\s*,\s*\(\w+\)\s*=>\s*reject\(\w+\)', updated)
if remaining:
    print('WARNING: Still has 4-arg patterns!')
    # Show context
    idx = remaining.start()
    print(updated[max(0, idx-50):idx+150])
else:
    print('All executeSql calls are now 3-arg (verified)')
