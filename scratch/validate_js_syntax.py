# -*- coding: utf-8 -*-
import sys
import re
import subprocess
import tempfile
import os

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all <script>...</script>
scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', html, re.DOTALL)
print(f"Found {len(scripts)} script tags in index.html")

all_ok = True
for idx, s in enumerate(scripts):
    # Ignore empty or CDN imports
    code = s.strip()
    if not code:
        continue
    
    with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8') as tf:
        tf.write(code)
        temp_js = tf.name
    
    try:
        # Check syntax using node --check
        res = subprocess.run(['node', '--check', temp_js], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"Script #{idx + 1} (len {len(code)} bytes): Syntax OK!")
        else:
            print(f"Script #{idx + 1} ERROR:")
            print(res.stderr)
            all_ok = False
    finally:
        if os.path.exists(temp_js):
            os.remove(temp_js)

if all_ok:
    print("ALL JAVASCRIPT BLOCKS PASSED SYNTAX CHECK!")
else:
    print("SOME JAVASCRIPT BLOCKS FAILED SYNTAX CHECK.")
