import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i, l in enumerate(lines):
    # Check for corrupt characters like dYs, ???, unusual ascii, or quotes
    if any(k in l for k in ['dYs', '???', '•••', '...', '…', ':::', '|||']):
        print(f"Line {i+1}: {l.strip()[:100]}")
