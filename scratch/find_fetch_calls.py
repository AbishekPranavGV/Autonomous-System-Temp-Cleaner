# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

fetches = re.findall(r'fetch\([^\)]+\)', text)
print("fetch calls found:")
for f in set(fetches):
    print(" -", f[:80])
