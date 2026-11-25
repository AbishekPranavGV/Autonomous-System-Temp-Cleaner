with open('cleaner.py', 'r', encoding='utf-8') as f:
    text = f.read()

print("cleaner.py lines:", len(text.split('\n')))
for l in text.split('\n'):
    if any(k in l for k in ['EXCLUDE', 'PROTECT', 'RETENTION', 'def ']):
        print(" ", l.strip()[:100])
