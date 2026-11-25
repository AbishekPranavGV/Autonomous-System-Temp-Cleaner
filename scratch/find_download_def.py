# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function downloadFreshClientZip')
if idx != -1:
    print(repr(text[idx:idx+500]))
else:
    print("function downloadFreshClientZip not found")
