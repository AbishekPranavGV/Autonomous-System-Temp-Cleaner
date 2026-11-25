# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

style_match = text.find('.app-window')
if style_match != -1:
    print(text[style_match-50:style_match+300])
else:
    print(".app-window not found in style")
