# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Header HTML ---")
for i in range(150, 290):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
