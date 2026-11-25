with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'(chartStorageTrajectory|dashboardTrajectoryChart)', text)
for m in matches:
    start = max(0, m.start() - 60)
    end = min(len(text), m.end() + 60)
    print(f"Match: {repr(text[start:end])}")
