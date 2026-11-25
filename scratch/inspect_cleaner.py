import re

with open('cleaner.py', 'r', encoding='utf-8') as f:
    text = f.read()

print('cleaner.py length:', len(text))
matches = re.findall(r'(def\s+[a-zA-Z0-9_]+|\bRETENTION\w*|\bVERSION\b)', text)
print('matches in cleaner.py:', matches[:20])
