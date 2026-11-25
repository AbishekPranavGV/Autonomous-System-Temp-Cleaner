# -*- coding: utf-8 -*-
import sys
import urllib.request
import json
import zipfile
import io

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

base_url = "https://autonomous-system-temp-cleaner-six.vercel.app"

# 1. Test Proxy /api/version
print(f"1. Testing Vercel -> Backend Proxy ({base_url}/api/version)...")
try:
    with urllib.request.urlopen(f"{base_url}/api/version", timeout=10) as resp:
        print(f"   Status: {resp.status}")
        print(f"   Response: {resp.read().decode('utf-8')[:150]}")
except Exception as e:
    print(f"   Proxy error: {e}")

# 2. Test Client Zip Download
print(f"\n2. Testing Client Zip Download ({base_url}/NUNES_FLEET_CLIENT_V7.zip)...")
try:
    with urllib.request.urlopen(f"{base_url}/NUNES_FLEET_CLIENT_V7.zip", timeout=15) as resp:
        print(f"   Status: {resp.status}")
        data = resp.read()
        print(f"   Downloaded size: {len(data):,} bytes")
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            names = zf.namelist()
            print(f"   Files inside zip ({len(names)}):")
            for n in names[:8]:
                print(f"     - {n}")
            has_start = 'START_AUTO_CLEANER.bat' in names
            has_agent = 'nunes_fleet_agent.ps1' in names
            print(f"   START_AUTO_CLEANER.bat present: {has_start}")
            print(f"   nunes_fleet_agent.ps1 present: {has_agent}")
except Exception as e:
    print(f"   Download error: {e}")

# 3. Test Live Fleet Sync in Dashboard HTML
print(f"\n3. Testing Live Fleet Polling in HTML ({base_url})...")
try:
    with urllib.request.urlopen(base_url, timeout=10) as resp:
        html = resp.read().decode('utf-8')
        has_sync_engine = 'pollLiveFleetStatus' in html
        has_dynamic_card = 'New Fleet Computer Connected' in html
        print(f"   Live sync engine in HTML: {has_sync_engine}")
        print(f"   Dynamic card builder in HTML: {has_dynamic_card}")
except Exception as e:
    print(f"   HTML error: {e}")
