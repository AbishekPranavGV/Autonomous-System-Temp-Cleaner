import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# find any three dots or dots in HTML (not inside script or style)
# remove script and style blocks first
no_script = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
no_style = re.sub(r'<style.*?</style>', '', no_script, flags=re.DOTALL)

for i, l in enumerate(no_style.split('\n')):
    if any(k in l for k in ['...', '…', '··', '••', '::', '||']):
        print(f"Line {i+1}: {l.strip()}")
