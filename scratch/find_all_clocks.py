# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'id=["\'][^"\']*clock[^"\']*["\']', text, re.I)
print("Clock element IDs:", matches)

matches2 = re.findall(r'LIVE\s*•[^<]*', text)
print("LIVE • matches:", matches2)
