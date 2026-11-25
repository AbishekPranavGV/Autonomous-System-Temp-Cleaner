import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('fleetNodesDetailedGrid')
end = c.find('</section>', pos)
print(c[pos:end])
