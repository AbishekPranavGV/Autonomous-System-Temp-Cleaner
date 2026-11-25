# -*- coding: utf-8 -*-
with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

print("Send-UniversalJsonGet in nunes_fleet_agent.ps1:", "Send-UniversalJsonGet" in text)
print("Send-UniversalJsonPost in nunes_fleet_agent.ps1:", "Send-UniversalJsonPost" in text)
