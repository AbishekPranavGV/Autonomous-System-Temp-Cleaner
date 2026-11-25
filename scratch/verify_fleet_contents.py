# -*- coding: utf-8 -*-
import sys
import urllib.request
import json

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with urllib.request.urlopen('http://127.0.0.1:8090/api/status') as r:
    res = json.loads(r.read())
    fleet_data = res.get('data', {})
    print("Total monitored:", fleet_data.get('total_monitored'))
    print("Online count:", fleet_data.get('online_count'))
    print("Today recovered MB:", fleet_data.get('today_recovered_mb'))
    print("Computers in fleet:")
    for c in fleet_data.get('fleet', []):
        print(f" - {c.get('computer')} ({c.get('status')}) Free: {c.get('disk_free_gb')} GB, Online: {c.get('online')}, Last Seen: {c.get('last_seen_utc')}")
