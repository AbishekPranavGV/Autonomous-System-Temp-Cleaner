# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

header_match = re.search(r'<header[^>]*>(.*?)</header>', text, re.DOTALL)
if header_match:
    header_content = header_match.group(1)
    print("Header length:", len(header_content))
    # print all top-level divs or buttons
    elements = re.findall(r'<!--\s*(.*?)\s*-->|<(button|div|input)[^>]*id=["\']([^"\']+)["\']', header_content)
    for el in elements[:25]:
        print(el)
