import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'(\.\.\.|…|···|""|\'\'\'|:::)', text)
for m in matches:
    start = max(0, m.start() - 40)
    end = min(len(text), m.end() + 40)
    print(f"Match at {m.start()}: {repr(text[start:end])}")
