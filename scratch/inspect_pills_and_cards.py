import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

pos1 = c.find('Fleet Filter Pills')
pos2 = c.find('<!-- Onboarding Any Windows Computer Box -->')
print(c[pos1:pos2])
