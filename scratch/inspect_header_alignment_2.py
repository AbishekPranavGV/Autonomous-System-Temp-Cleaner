# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Lines 290-370 ---")
for i in range(289, min(370, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
