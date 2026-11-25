import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_url = "http://127.0.0.1:8090"
tests = [
    ("/api/status", "GET", None),
    ("/api/diagnostics", "GET", None),
    ("/api/analytics", "GET", None),
    ("/api/prompt_backups", "GET", None),
    ("/api/live_files?limit=10", "GET", None),
    ("/api/ai/chat", "POST", {"message": "Why is my computer slow?", "node": "DESKTOP-M378M07", "lang": "en"}),
    ("/api/ai/chat", "POST", {"message": "கணினி ஏன் மெதுவாக உள்ளது?", "node": "DESKTOP-M378M07", "lang": "ta"}),
    ("/api/ai/chat", "POST", {"message": "Which NUNES computer needs attention?", "node": "DESKTOP-M378M07", "lang": "en"}),
    ("/api/ai/chat", "POST", {"message": "Why is the Accounts PC freezing?", "node": "DESKTOP-EV2F0TV", "lang": "en"}),
]

all_passed = True
for path, method, body in tests:
    url = base_url + path
    try:
        data = json.dumps(body).encode('utf-8') if body else None
        headers = {'Content-Type': 'application/json'} if body else {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=5) as res:
            res_data = json.loads(res.read().decode('utf-8'))
            print(f"[PASS] {method} {path} -> HTTP {res.status}")
    except Exception as e:
        print(f"[FAIL] {method} {path} -> Error: {e}")
        all_passed = False

if all_passed:
    print("\nALL ENDPOINTS RETURNED 200 OK & VALID JSON!")
else:
    print("\nSOME ENDPOINTS FAILED!")
    sys.exit(1)
