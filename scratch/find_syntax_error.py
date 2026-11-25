# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("k === 'downloadclient'")
if idx != -1:
    print(text[idx-200:idx+200])
