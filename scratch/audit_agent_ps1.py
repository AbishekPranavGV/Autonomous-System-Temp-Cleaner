with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

print("nunes_fleet_agent.ps1 lines:", len(text.split('\n')))
for l in text.split('\n'):
    if any(k in l for k in ['function ', 'param(', '$LOOP_INTERVAL', '$RETENTION', '$VERSION']):
        print(" ", l.strip()[:100])
