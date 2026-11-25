# -*- coding: utf-8 -*-
import sys
import urllib.request
import json

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

endpoints = [
    ('/', 'GET', None),
    ('/api/status', 'GET', None),
    ('/api/version', 'GET', None),
    ('/api/diagnostics', 'GET', None),
    ('/api/notifications', 'GET', None),
    ('/api/fleet/node_details?node=DESKTOP-M378M07', 'GET', None),
    ('/api/reports/export?format=json', 'GET', None),
    ('/api/reports/export?format=csv', 'GET', None),
    ('/api/ai/chat', 'POST', {'message': 'Why is this computer slow?'}),
    ('/api/ai/chat', 'POST', {'message': 'இந்த கம்ப்யூட்டர் ஏன் மெதுவாக உள்ளது?'}),
]

for ep, method, payload in endpoints:
    url = f"http://127.0.0.1:8090{ep}"
    try:
        data = json.dumps(payload).encode('utf-8') if payload else None
        headers = {'Content-Type': 'application/json'} if payload else {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            content = resp.read()
            print(f"[{status}] {method} {ep} -> {len(content)} bytes")
            if 'ai/chat' in ep:
                res_obj = json.loads(content.decode('utf-8'))
                ans = res_obj.get('response', '')[:80].encode('ascii', errors='replace').decode('ascii')
                print("   AI Response:", ans, "...")
    except Exception as e:
        print(f"[FAIL] {method} {ep} -> {e}")
