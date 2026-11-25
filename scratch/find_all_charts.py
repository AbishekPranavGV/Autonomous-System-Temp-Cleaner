import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

canvases = re.findall(r'<canvas[^>]*id=["\']([^"\']+)["\']', c)
print('Canvases in index.html:', canvases)

charts = re.findall(r'new Chart\s*\(\s*([^,\n]+)', c)
print('Chart initializations:', [ch.strip() for ch in charts])
