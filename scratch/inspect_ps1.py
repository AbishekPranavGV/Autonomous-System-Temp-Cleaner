import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip()]

print(f"Total non-blank lines in nunes_fleet_agent.ps1: {len(lines)}")
for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['version', 'retention', '8.5.0', '35']):
        print(f"Line {i+1}: {l[:100]}")
