import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(340, 410):
    if i < len(lines):
        print(f"{i+1}: {lines[i].rstrip()}")
