# -*- coding: utf-8 -*-
with open('zip_builder.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines[15:45]):
    print(f"{i+16}: {l.strip()}")
