# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

head_idx = text.find('<head>')
head_end = text.find('</head>')
print(text[head_idx:head_idx+1500])
