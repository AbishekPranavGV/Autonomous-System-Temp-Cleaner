# -*- coding: utf-8 -*-
import sys
import urllib.request

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://nam-usr-concerns-incidents.trycloudflare.com/api/version"
try:
    with urllib.request.urlopen(url, timeout=10) as resp:
        print("Tunnel status:", resp.status)
        print("Tunnel response:", resp.read().decode('utf-8'))
except Exception as e:
    print("Tunnel error:", e)
