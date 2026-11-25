# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(6140, min(6250, len(lines))):
    if lines[i].strip():
        print(f"{i+1}: {lines[i]}", end='')
