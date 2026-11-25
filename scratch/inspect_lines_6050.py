# -*- coding: utf-8 -*-
with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(6050, 6080):
    if lines[i].strip():
        print(f"{i+1}: {repr(lines[i].strip())}")
