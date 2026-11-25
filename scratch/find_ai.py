import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'aiModal' in line or 'aiChat' in line or 'aiAssistant' in line or 'toggleAIAssistant' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
