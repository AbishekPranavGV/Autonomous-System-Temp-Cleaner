# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

canvases = re.findall(r'<canvas[^>]*id=["\']([^"\']+)["\']', text)
print("Canvas IDs found in index.html:", canvases)

charts = re.findall(r'new\s+Chart\s*\(\s*([^,\)]+)', text)
print("Chart initializations found:", charts)
