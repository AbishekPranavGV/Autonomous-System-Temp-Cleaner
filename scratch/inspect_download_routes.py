# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1190, min(1230, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
