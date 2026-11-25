texts = [
    'Mica Light & Obsidian Suite',
    'tempfileremover.com',
    '• NUNES Fleet v8.5.0 Quantum',
    'Administrator access detected',
    'License activated',
    '4H Loop:',
    'No scan yet'
]

for fname in ['index.html', 'dashboard/templates/index.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f'=== {fname} ===')
    for t in texts:
        count = content.count(t)
        print(f'  "{t}": {count} occurrences')
