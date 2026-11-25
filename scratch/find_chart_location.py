import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'chartStorageTrajectory' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(max(0, i-5), min(len(lines), i+15)):
            print(f"  {j+1}: {lines[j].rstrip()}")
