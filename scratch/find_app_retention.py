import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

for i, line in enumerate(text.splitlines(), 1):
    if '35' in line or 'retention' in line.lower() or '8.5.0' in line:
        print(f"Line {i}: {line.strip()[:100]}")
