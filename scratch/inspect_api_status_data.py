# -*- coding: utf-8 -*-
import sys
import urllib.request
import json

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with urllib.request.urlopen('http://127.0.0.1:8090/api/status') as r:
    data = json.loads(r.read())
    print("Keys in /api/status:", list(data.keys()))
    print("Sample content:\n", json.dumps(data, indent=2)[:500])
