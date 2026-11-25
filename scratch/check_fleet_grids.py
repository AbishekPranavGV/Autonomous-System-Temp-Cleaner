# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

grids = re.findall(r'<div[^>]*id=["\']([^"\']*(?:fleet|nodes|grid)[^"\']*)["\'][^>]*class=["\']([^"\']+)["\']', text, re.I)
for g in grids:
    print(g)
