import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('Length of index.html:', len(html))
headings = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html)
for h in headings[:25]:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    if clean:
        print('Heading:', clean)
