# -*- coding: utf-8 -*-
with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(4570, min(4700, len(lines))):
    if lines[i].strip():
        print(f"{i+1}: {lines[i].strip()}")
