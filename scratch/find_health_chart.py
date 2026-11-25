import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('chartStorageTrajectory')
while pos != -1:
    print('Found chartStorageTrajectory at', pos)
    print(c[pos-50:pos+300])
    pos = c.find('chartStorageTrajectory', pos+1)
