# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

for p in ['index.html', 'dashboard/templates/index.html']:
    with open(p, 'r', encoding='utf-8') as f:
        t = f.read()
    
    clock_html = re.findall(r'<div[^>]*title=["\'][^"\']*Coimbatore[^"\']*["\'][^>]*>.*?</div>', t, re.DOTALL)
    print(f"=== {p} ===")
    if clock_html:
        print("Clock HTML:\n", clock_html[0].strip())
    else:
        print("Clock with Coimbatore not found")
    
    # Check updateClock function in JS
    fn_match = re.search(r'function updateClock\(\)\s*\{.*?\}', t, re.DOTALL)
    if fn_match:
        print("updateClock JS:\n", fn_match.group(0))
