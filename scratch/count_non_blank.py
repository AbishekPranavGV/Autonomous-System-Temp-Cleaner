with open('index.html', 'r', encoding='utf-8') as f:
    lines = [l for l in f if l.strip()]

print(f"Total non-blank lines: {len(lines)}")
