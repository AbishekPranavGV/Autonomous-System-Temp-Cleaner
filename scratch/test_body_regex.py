# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Check body tag
body_pat = r'<body\s+class="[^"]*"\s*flex\s+overflow-hidden>'
m = re.search(body_pat, content)
print("Found body tag with outside flex overflow-hidden:", bool(m))
if m:
    print("Matched:", m.group(0))
