import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

tokens = ['...', '..', '. . .', '---', '"""', "'''", '|||', ':::']
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped in tokens:
        print(f'Stray token at line {i+1}: {repr(stripped)}')
    if re.match(r'^\s*[\.\:\-\|]{2,}\s*$', line):
        print(f'Stray punctuation at line {i+1}: {repr(line)}')
print('Search complete across', len(lines), 'lines in index.html')
