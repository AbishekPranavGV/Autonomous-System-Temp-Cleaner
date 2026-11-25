import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('function openNodeDetailDrawer')
if pos != -1:
    print(c[pos:pos+1200])
else:
    print('openNodeDetailDrawer not found')
