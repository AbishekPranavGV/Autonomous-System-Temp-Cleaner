# -*- coding: utf-8 -*-
with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Connected to Dashboard at' in l:
        print(f"Line {i+1}:")
        for j in range(max(0, i-5), min(len(lines), i+15)):
            print(f"  {j+1}: {lines[j].strip()}")
