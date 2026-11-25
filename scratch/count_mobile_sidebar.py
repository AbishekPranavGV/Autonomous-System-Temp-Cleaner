# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

count = text.count('toggleMobileSidebar()')
print("Count of toggleMobileSidebar() in index.html:", count)
