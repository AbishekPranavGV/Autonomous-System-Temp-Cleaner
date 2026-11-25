# -*- coding: utf-8 -*-
new_tunnel = 'margaret-operate-chemistry-zshops.trycloudflare.com'

# 1. Update api/[...path].js
with open('api/[...path].js', 'r', encoding='utf-8') as f:
    c = f.read()
import re
c = re.sub(r"const BACKEND_HOST = '[^']+';", f"const BACKEND_HOST = '{new_tunnel}';", c)
with open('api/[...path].js', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated api/[...path].js")

# 2. Update dashboard/data/tunnel.json
import json
with open('dashboard/data/tunnel.json', 'w', encoding='utf-8') as f:
    json.dump({"url": f"https://{new_tunnel}", "status": "ONLINE"}, f, indent=2)
print("Updated dashboard/data/tunnel.json")

# 3. Update nunes_fleet_agent.ps1
with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    c_ps = f.read()
c_ps = re.sub(r'https://[^"]+\.trycloudflare\.com', f'https://{new_tunnel}', c_ps)
with open('nunes_fleet_agent.ps1', 'w', encoding='utf-8') as f:
    f.write(c_ps)
print("Updated nunes_fleet_agent.ps1")
