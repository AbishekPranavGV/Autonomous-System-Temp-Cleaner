# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('zip_builder.py', 'r', encoding='utf-8') as f:
    print(f.read())
