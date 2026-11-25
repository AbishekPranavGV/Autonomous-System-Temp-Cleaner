import sys
from pathlib import Path
import shutil

sys.stdout.reconfigure(encoding='utf-8')

import gen_part1
import gen_part2
import gen_part3
import gen_part4
import gen_part5

full_html = (
    gen_part1.HEAD_HTML +
    gen_part2.BODY_HEADER_NAV +
    gen_part3.SECTIONS_1_2_3 +
    gen_part4.SECTIONS_4_5_6_7_8 +
    gen_part5.MODALS_AND_SCRIPTS
)

root_dir = Path(__file__).resolve().parent.parent
target_root = root_dir / 'index.html'
target_dashboard = root_dir / 'dashboard' / 'templates' / 'index.html'

with open(target_root, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f"Wrote {len(full_html)} chars to {target_root}")

with open(target_dashboard, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f"Wrote {len(full_html)} chars to {target_dashboard}")
