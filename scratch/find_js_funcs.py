import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', html)
print(f"Total functions in index.html: {len(funcs)}")
print("Sample functions:", funcs[:35])
