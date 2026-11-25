import inspect
import sys
import os

with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    app_text = f.read()

import re
routes = re.findall(r'@app\.route\([\'"]([^\'"]+)[\'"](?:,\s*methods=\[([^\]]+)\])?\)', app_text)
print("--- ALL FLASK ROUTES ---")
for r, m in routes:
    methods = m.replace("'", "").replace('"', '') if m else 'GET'
    print(f"Route: {r:35} Methods: {methods}")

print("\n--- DATABASE / STATE PERSISTENCE ---")
for line in app_text.split('\n'):
    if any(k in line for k in ['DATA_DIR', 'fleet_cache', 'requests', 'results', 'queues', 'prompt_backups']):
        if len(line.strip()) < 100:
            print(line.strip())
