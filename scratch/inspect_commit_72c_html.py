import subprocess

res = subprocess.run(['git', 'show', '72c0342:index.html'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
html = res.stdout

# Look for dashboard or chart in 72c0342
for line in html.split('\n'):
    if any(k in line.lower() for k in ['dashboard', 'chart', 'graph', 'modal', 'drawer']):
        if len(line.strip()) < 150:
            print(line.strip())
