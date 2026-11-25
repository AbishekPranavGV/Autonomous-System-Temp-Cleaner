# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Lines 260-275 ---")
for i in range(259, min(275, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')

print("\n--- Lines 3090-3115 ---")
for i in range(3089, min(3115, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
