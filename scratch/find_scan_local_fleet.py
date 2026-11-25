import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('def scan_local_fleet')
print(text[idx:idx+1500])
