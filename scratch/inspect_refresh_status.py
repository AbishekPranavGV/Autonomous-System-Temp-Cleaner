# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function refreshStatus')
if idx == -1:
    idx = text.find('refreshFleet')
if idx != -1:
    print(text[idx:idx+2500])
else:
    print("refreshStatus not found, searching for /api/status")
    for m in re.finditer(r'/api/status', text):
        pos = m.start()
        print(text[pos-100:pos+300])
        print("="*40)
