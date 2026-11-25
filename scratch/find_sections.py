import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines):
    if '<header' in line or '<nav' in line or '<main' in line or '<footer' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
    if 'id=' in line and any(k in line for k in ['modal', 'panel', 'dashboard', 'chat', 'fleet', 'analytics', 'settings']):
        print(f"Line {i+1} [ID]: {line.strip()[:100]}")
