# -*- coding: utf-8 -*-
import os

old_urls = [
    'republic-medical-incoming-convert.trycloudflare.com',
    'wrestling-contract-dropped-incorporate.trycloudflare.com'
]
new_url = 'nam-usr-concerns-incidents.trycloudflare.com'

files_to_update = [
    'nunes_fleet_agent.ps1',
    'nunes_universal_cleaner.py',
    'show_status.ps1',
    'dashboard/data/tunnel.json',
    'README_SETUP.txt',
    'Autonomous-System-Temp-Cleaner-COPY.json'
]

for fp in files_to_update:
    if not os.path.exists(fp):
        print(f"Skipping {fp}, not found")
        continue
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    modified = False
    for old in old_urls:
        if old in content:
            content = content.replace(old, new_url)
            modified = True
            print(f"Replaced {old} in {fp}")
            
    if modified:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {fp}")
