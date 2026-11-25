# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'CandidateUrls' in l or 'trycloudflare' in l or 'Find-Active' in l or 'Invoke-RestMethod' in l or 'api/sync' in l or 'api/report' in l or 'api/status' in l:
        print(f"Line {i+1}: {l.strip()}")
