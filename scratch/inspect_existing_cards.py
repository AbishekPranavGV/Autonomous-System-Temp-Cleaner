# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for pc in ['DESKTOP-M378M07', 'DESKTOP-EV2F0TV', 'DESKTOP-I2MHDIB', 'DESKTOP-F8G3T2C']:
    idx = text.find(f'data-node="{pc}"')
    if idx != -1:
        print(f"=== {pc} ===")
        print(text[idx:idx+800])
