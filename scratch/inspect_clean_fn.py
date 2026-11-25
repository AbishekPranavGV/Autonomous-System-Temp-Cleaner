# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function Invoke-SystemClean' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(i+100, len(lines))):
            if 'Send-Heartbeat' in lines[j] or 'Send-Report' in lines[j]:
                print(f"  Line {j+1}: {lines[j].strip()}")
