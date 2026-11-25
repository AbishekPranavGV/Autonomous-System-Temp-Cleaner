# -*- coding: utf-8 -*-
import sys
import os
import re
import json
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ACTIVE_TUNNEL = 'https://margaret-operate-chemistry-zshops.trycloudflare.com'
VERCEL_URL = 'https://autonomous-system-temp-cleaner-six.vercel.app'

print(f"[*] Configuring live everywhere: {ACTIVE_TUNNEL}")

# 1. Update dashboard/data/tunnel.json
tunnel_json_p = Path('dashboard/data/tunnel.json')
with open(tunnel_json_p, 'w', encoding='utf-8') as f:
    json.dump({"url": ACTIVE_TUNNEL, "status": "ONLINE"}, f, indent=2)
print(" [OK] Updated dashboard/data/tunnel.json")

# 2. Add /api/tunnel route to dashboard/app.py
with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

if "@app.route('/api/tunnel')" not in app_code:
    tunnel_route = """
@app.route('/api/tunnel')
def api_tunnel():
    \"\"\"Returns the active global Cloudflare tunnel URL so all fleet clients discover it dynamically.\"\"\"
    tunnel_file = DATA_DIR / 'tunnel.json'
    url = '""" + ACTIVE_TUNNEL + """'
    status = 'ONLINE'
    if tunnel_file.exists():
        try:
            with open(tunnel_file, 'r', encoding='utf-8') as f:
                t = json.load(f)
                url = t.get('url', url)
                status = t.get('status', status)
        except Exception:
            pass
    return jsonify({
        'success': True,
        'tunnel_url': url,
        'status': status
    })
"""
    app_code = app_code.replace("@app.route('/api/version')", tunnel_route + "\n@app.route('/api/version')")
    with open('dashboard/app.py', 'w', encoding='utf-8') as f:
        f.write(app_code)
    print(" [OK] Added /api/tunnel to dashboard/app.py")

# 3. Update nunes_fleet_agent.ps1 with Send-UniversalJsonGet and Dynamic Discovery
with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    ps1 = f.read()

# Candidate URLs update
candidate_block = f"""# Candidate Dashboard URLs across Cloud Tunnel, Vercel Edge, LAN & Tailscale
$CandidateUrls = @(
    "{ACTIVE_TUNNEL}",
    "{VERCEL_URL}",
    "http://100.88.183.106:8090",
    "http://192.168.1.114:8090",
    "http://192.168.0.100:8090",
    "http://192.168.29.88:8090",
    "http://localhost:8090"
)"""

ps1 = re.sub(
    r'# Candidate Dashboard URLs across Cloud Tunnel[^\)]+\)',
    candidate_block,
    ps1,
    flags=re.DOTALL
)

# Add Send-UniversalJsonGet function if not present
json_get_fn = """function Send-UniversalJsonGet {
    param(
        [Parameter(Mandatory=$true)][string]$Url,
        [int]$TimeoutSeconds = 3
    )
    if (Get-Command Invoke-RestMethod -ErrorAction SilentlyContinue) {
        try {
            return (Invoke-RestMethod -Uri $Url -Method Get -TimeoutSec $TimeoutSeconds -ErrorAction Stop)
        } catch {}
    }
    try {
        $wc = New-Object System.Net.WebClient
        $wc.Headers.Add("User-Agent", "NunesFleetAgent/10.1 (Windows; Universal)")
        $raw = $wc.DownloadString($Url)
        if ($raw -and (Get-Command ConvertFrom-Json -ErrorAction SilentlyContinue)) {
            return ($raw | ConvertFrom-Json)
        }
    } catch {}
    return $null
}
"""

if "function Send-UniversalJsonGet" not in ps1:
    ps1 = ps1.replace("function Send-UniversalJsonPost", json_get_fn + "\nfunction Send-UniversalJsonPost")
    print(" [OK] Added Send-UniversalJsonGet to nunes_fleet_agent.ps1")

# Add Dynamic Discovery call before Send-Report execution
dynamic_discovery_code = f"""# Dynamic Tunnel Discovery: Query permanent Vercel domain for current live tunnel
try {{
    $dynResp = Send-UniversalJsonGet -Url "{VERCEL_URL}/api/tunnel" -TimeoutSeconds 3
    if ($dynResp -and $dynResp.tunnel_url) {{
        $liveUrl = $dynResp.tunnel_url.Trim().TrimEnd('/')
        if ($liveUrl -and -not ($CandidateUrls -contains $liveUrl)) {{
            $CandidateUrls = @($liveUrl) + $CandidateUrls
        }}
    }}
}} catch {{}}
"""

if "Dynamic Tunnel Discovery:" not in ps1:
    ps1 = ps1.replace(
        "if ($DashboardUrl) {",
        dynamic_discovery_code + "\nif ($DashboardUrl) {"
    )
    print(" [OK] Added Dynamic Discovery on agent startup")

# Cache successful working URL in Send-Report
cache_working_url = """                Write-Host "   [OK] Connected to Dashboard at: $baseUrl" -ForegroundColor Green
                Write-Host "   [OK] Fleet registration confirmed for $($Telemetry.Computer)!" -ForegroundColor Green
                # Move working URL to top of candidate list for fast future heartbeats
                $Script:CandidateUrls = @($baseUrl) + ($CandidateUrls | Where-Object { $_ -ne $baseUrl })"""

old_success_lines = """                Write-Host "   [OK] Connected to Dashboard at: $baseUrl" -ForegroundColor Green
                Write-Host "   [OK] Fleet registration confirmed for $($Telemetry.Computer)!" -ForegroundColor Green"""

if old_success_lines in ps1 and "$Script:CandidateUrls = @($baseUrl)" not in ps1:
    ps1 = ps1.replace(old_success_lines, cache_working_url)
    print(" [OK] Added working URL auto-prioritization to Send-Report")

with open('nunes_fleet_agent.ps1', 'w', encoding='utf-8') as f:
    f.write(ps1)

# 4. Update README_SETUP.txt
with open('README_SETUP.txt', 'r', encoding='utf-8') as f:
    readme = f.read()

readme = re.sub(r'Cloudflare Live Tunnel\s*:\s*https?://[^\s\n]+', f'Cloudflare Live Tunnel    : {ACTIVE_TUNNEL}', readme)
with open('README_SETUP.txt', 'w', encoding='utf-8') as f:
    f.write(readme)
print(" [OK] Updated README_SETUP.txt")

# 5. Rebuild Client ZIPs
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import zip_builder
zip_builder.build_client_zip(verbose=True)

print("[SUCCESS] All files and ZIP packages updated for live connection everywhere!")
