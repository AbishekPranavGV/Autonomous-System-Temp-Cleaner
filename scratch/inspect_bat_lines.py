# -*- coding: utf-8 -*-
with open('CONNECT_THIS_PC.bat', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines[20:70]):
    print(f"{i+21}: {l.strip()}")
