# -*- coding: utf-8 -*-
import sys
import urllib.request
import json
import zipfile
import io

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

base = "https://autonomous-system-temp-cleaner-six.vercel.app"

# 1. Test /api/tunnel
print("1. Testing Dynamic Discovery Endpoint (/api/tunnel)...")
try:
    with urllib.request.urlopen(f"{base}/api/tunnel", timeout=10) as r:
        print(f"   Status: {r.status}")
        data = json.loads(r.read())
        print(f"   Tunnel URL: {data.get('tunnel_url')}")
        print(f"   Status: {data.get('status')}")
except Exception as e:
    print(f"   Error: {e}")

# 2. Test Download of updated ZIP
print("\n2. Testing Updated ZIP File Download (/NUNES_FLEET_CLIENT_V7.zip)...")
try:
    with urllib.request.urlopen(f"{base}/NUNES_FLEET_CLIENT_V7.zip", timeout=15) as r:
        print(f"   Status: {r.status}")
        zip_bytes = r.read()
        print(f"   Downloaded Size: {len(zip_bytes):,} bytes")
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            ps1_code = zf.read('nunes_fleet_agent.ps1').decode('utf-8')
            has_dyn = 'Dynamic Tunnel Discovery:' in ps1_code
            has_get = 'function Send-UniversalJsonGet' in ps1_code
            has_cache = '$Script:CandidateUrls = @($baseUrl)' in ps1_code
            print(f"   nunes_fleet_agent.ps1 Dynamic Discovery Present: {has_dyn}")
            print(f"   nunes_fleet_agent.ps1 Send-UniversalJsonGet Present: {has_get}")
            print(f"   nunes_fleet_agent.ps1 Auto-Prioritization Present: {has_cache}")
except Exception as e:
    print(f"   Error: {e}")
