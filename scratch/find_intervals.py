# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for any interval or polling function
intervals = re.findall(r'setInterval\([^\)]+\)', text)
print("setInterval calls found:")
for i in intervals:
    print(" -", i)
