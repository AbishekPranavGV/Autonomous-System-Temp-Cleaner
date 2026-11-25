# -*- coding: utf-8 -*-
with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    for i, l in enumerate(f):
        if 'trycloudflare' in l:
            print(f"{i+1}: {l.strip()}")
