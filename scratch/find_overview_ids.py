# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="sec_overview"')
if idx != -1:
    sub = text[idx:idx+3500]
    ids = re.findall(r'id=["\']([^"\']+)["\']', sub)
    print("Element IDs in sec_overview:")
    for i in ids:
        print(" -", i)
