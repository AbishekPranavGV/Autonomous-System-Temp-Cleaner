# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('id="sec_fleet"')
if idx1 != -1:
    print("--- sec_fleet ---")
    print(text[idx1:idx1+1200])

idx2 = text.find('id="sec_overview"')
if idx2 != -1:
    print("--- sec_overview fleet ---")
    sub = text[idx2:idx2+4000]
    p = sub.find('DESKTOP-M378M07')
    if p != -1:
        print(sub[p-300:p+500])
