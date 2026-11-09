"""Fix remaining HomePage onClick -> onTap in TabItem usage."""
fp = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets\pages\HomePage.ets'
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
orig = text

# The TabItem calls still use onClick instead of onTap
# Replace onClick -> onTap in TabItem constructor calls
import re
text = re.sub(r'TabItem\(\{[^}]+\}\)', lambda m: m.group(0).replace('onClick', 'onTap'), text)

if text != orig:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed HomePage TabItem onClick -> onTap')
else:
    # The usage pattern might be different
    # Let's try a different approach
    text = text.replace('onClick:', 'onTap:')
    if text != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(text)
        print('Fixed HomePage onClick -> onTap (direct replace)')
    else:
        print('No changes needed')
