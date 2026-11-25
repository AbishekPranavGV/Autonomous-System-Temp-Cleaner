import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update version to 10.0.0
text = text.replace('v8.5.0 Quantum Hyper-Fleet Sentinel', 'v10.0.0 Enterprise Command Center')
text = text.replace('v8.5.0', 'v10.0.0')
text = text.replace('Version = "8.5.0"', 'Version = "10.0.0"')

# 2. Update retention to 30 days
text = text.replace('35-Day Retention', '30-Day Retention')
text = text.replace('35-day retention', '30-day retention')
text = text.replace('older than 35 days', 'older than 30 days')
text = text.replace('.AddDays(-35)', '.AddDays(-30)')

with open('nunes_fleet_agent.ps1', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated nunes_fleet_agent.ps1 successfully!")
