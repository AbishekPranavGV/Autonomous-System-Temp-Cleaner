# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

count = text.count('btnHeaderDashboard')
print("Occurrences of btnHeaderDashboard:", count)
