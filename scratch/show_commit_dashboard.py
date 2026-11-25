import subprocess
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

res = subprocess.run(['git', 'show', '72c0342:index.html'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
lines = res.stdout.split('\n')

for i, l in enumerate(lines):
    if 'dashboardFleetSection' in l or '<!-- Dashboard Button -->' in l:
        print(f"--- Around line {i+1} ---")
        for j in range(max(0, i-5), min(len(lines), i+35)):
            print(f"{j+1}: {lines[j]}")
