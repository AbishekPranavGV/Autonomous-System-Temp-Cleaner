# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

count = text.count('Department:')
print("Occurrences of 'Department:' in index.html:", count)
if count > 0:
    for line in text.splitlines():
        if 'Department:' in line:
            print("Found in line:", line.strip())
