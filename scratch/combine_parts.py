import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
scratch_dir = root_dir / 'scratch'

parts = [
    scratch_dir / 'part1.html',
    scratch_dir / 'part2.html',
    scratch_dir / 'part3.html',
    scratch_dir / 'part4.html',
    scratch_dir / 'part5.html'
]

combined = []
for p in parts:
    with open(p, 'r', encoding='utf-8') as f:
        combined.append(f.read())

full_html = "".join(combined)

target_root = root_dir / 'index.html'
target_dashboard = root_dir / 'dashboard' / 'templates' / 'index.html'

with open(target_root, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f"Successfully generated {target_root} ({len(full_html)} bytes)")

with open(target_dashboard, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f"Successfully synced {target_dashboard} ({len(full_html)} bytes)")
