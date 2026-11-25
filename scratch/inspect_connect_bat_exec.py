# -*- coding: utf-8 -*-
with open('CONNECT_THIS_PC.bat', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[270:370]):
    if l.strip():
        print(f"{i+271}: {l.strip()}")
