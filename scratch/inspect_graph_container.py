import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('STORAGE CAPACITY TRAJECTORY (GB)')
print(c[pos-250:pos+1500])
