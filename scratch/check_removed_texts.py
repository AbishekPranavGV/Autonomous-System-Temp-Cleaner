# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

checks = [
    'Mica Light & Obsidian Suite',
    'tempfileremover.com • NUNES Fleet v8.5.0',
    'Administrator access detected',
    'License activated',
    'No scan yet'
]

for c in checks:
    print(f"'{c}': {text.count(c)} occurrences")
