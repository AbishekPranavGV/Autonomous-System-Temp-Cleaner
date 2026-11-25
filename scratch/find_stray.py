import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
texts = re.findall(r'>([^<]+)<', text)
for t in texts:
    s = t.strip()
    if s and (s in ["'''", '"""', '...', '···', '..', '`', '---', ',,,', ':::'] or len(s) <= 4 and all(c in ".'\"`,-;:!?" for c in s)):
        print(f"Suspicious short text: {repr(s)}")
