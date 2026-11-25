# -*- coding: utf-8 -*-
with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(665, 685):
    print(f"{i+1}: {lines[i]}", end='')
