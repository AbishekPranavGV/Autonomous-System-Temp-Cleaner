# -*- coding: utf-8 -*-
import json
from pathlib import Path

cache_p = Path('dashboard/data/fleet_cache.json')
if cache_p.exists():
    with open(cache_p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fleet = [c for c in data.get('fleet', []) if c.get('computer') != 'TEST-REMOTE-LAPTOP']
    data['fleet'] = fleet
    data['total_monitored'] = len(fleet)
    data['online_count'] = len([c for c in fleet if c.get('online')])
    
    with open(cache_p, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Cleaned fleet_cache.json, fleet count:", len(fleet))
