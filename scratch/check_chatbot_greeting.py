# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for the chatbot welcome message
m = re.findall(r'(?:Hey there!|Hello!|I am your Fluxyn).*?(?:question|\!)', text, re.DOTALL)
for res in m[:3]:
    print("Found greeting match:\n", res[:200])
