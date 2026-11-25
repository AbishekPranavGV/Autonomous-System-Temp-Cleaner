# -*- coding: utf-8 -*-
import sys
import urllib.request
import json

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

test_payload = {
    "status": {
        "Computer": "TEST-REMOTE-LAPTOP",
        "User": "WorkUser",
        "OS": "Windows 11 Pro 64-bit",
        "Status": "ONLINE",
        "Online": True,
        "Version": "10.1.0",
        "DiskTotalGB": 512.0,
        "DiskFreeGB": 85.5,
        "DiskPercentUsed": 83.3,
        "LocalIPv4": "192.168.1.55",
        "TailscaleIP": "",
        "NetworkMode": "INTERNET_PUBLIC",
        "AutoCleanEnabled": True
    },
    "result": {
        "Computer": "TEST-REMOTE-LAPTOP",
        "DeletedFiles": 1420,
        "ReclaimedMB": 820.5,
        "FreeSpaceAfterGB": 85.5,
        "Status": "SUCCESS",
        "Trigger": "INITIAL_AUTONOMOUS_CONNECT"
    }
}

# Test 1: Direct Local
url_local = "http://127.0.0.1:8090/api/report"
print(f"Testing local: {url_local}")
try:
    req = urllib.request.Request(url_local, data=json.dumps(test_payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=5) as r:
        print("Local response:", r.status, r.read().decode('utf-8'))
except Exception as e:
    print("Local error:", e)

# Test 2: Via Cloudflare Tunnel (Worldwide Access)
url_tunnel = "https://nam-usr-concerns-incidents.trycloudflare.com/api/report"
print(f"\nTesting Cloudflare Tunnel: {url_tunnel}")
try:
    req = urllib.request.Request(url_tunnel, data=json.dumps(test_payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as r:
        print("Tunnel response:", r.status, r.read().decode('utf-8'))
except Exception as e:
    print("Tunnel error:", e)
