with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i, l in enumerate(lines):
    if 'chartStorageTrajectory' in l or 'chartCategoryDistribution' in l:
        print(f"Line {i+1}: {l.strip()[:100]}")
