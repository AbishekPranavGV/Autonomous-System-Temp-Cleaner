# -*- coding: utf-8 -*-
import sys
import urllib.request
import json

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with urllib.request.urlopen('http://127.0.0.1:8090/api/status') as r:
    data = json.loads(r.read())
    print("Total monitored:", data.get('total_monitored'))
    print("Computers:")
    for c in data.get('fleet', []):
        print(f" - {c.get('computer')} ({c.get('status')}) Free: {c.get('disk_free_gb')} GB, Online: {c.get('online')}")
