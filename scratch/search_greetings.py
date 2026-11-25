import sys
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['index.html', 'dashboard/templates/index.html', 'dashboard/ai_agent.py']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f'=== {fname} ===')
    for i, line in enumerate(content.splitlines()):
        if any(w in line for w in ['Fluxyn', 'Hello! I am', 'Hey there!']):
            print(f'  Line {i+1}: {line.strip()[:100]}')
