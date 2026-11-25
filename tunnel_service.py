"""
NUNES AUTONOMOUS TUNNEL MONITOR & VERCEL EDGE PROXY SYNCHRONIZER
Continuously manages cloudflared tunnel, ensures the edge reverse proxy on Vercel
is always linked to the active endpoint, and rebuilds the client packages dynamically.
"""

import os
import sys
import time
import re
import json
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
CLOUDFLARED_BIN = r"C:\Program Files (x86)\cloudflared\cloudflared.exe"

def update_vercel_config(tunnel_url):
    domain = tunnel_url.replace("https://", "").replace("http://", "").strip("/")
    api_dir = ROOT_DIR / "api"
    api_dir.mkdir(parents=True, exist_ok=True)
    proxy_file = api_dir / "[...path].js"
    proxy_code = f"""const https = require('https');

const BACKEND_HOST = '{domain}';

module.exports = (req, res) => {{
  let path = req.url || '/';
  if (!path.startsWith('/api')) {{
    path = '/api' + (path.startsWith('/') ? path : '/' + path);
  }}

  const options = {{
    hostname: BACKEND_HOST,
    port: 443,
    path: path,
    method: req.method,
    headers: {{
      ...req.headers,
      host: BACKEND_HOST,
    }},
  }};

  const proxyReq = https.request(options, (proxyRes) => {{
    res.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(res);
  }});

  proxyReq.on('error', (err) => {{
    res.writeHead(502, {{ 'Content-Type': 'application/json' }});
    res.end(JSON.stringify({{ error: err.message }}));
  }});

  req.pipe(proxyReq);
}};
"""
    with open(proxy_file, "w", encoding="utf-8") as f:
        f.write(proxy_code)
    print(f"[OK] Updated node proxy api/[...path].js for: {domain}")

def update_client_scripts(tunnel_url):
    # Update nunes_fleet_agent.ps1
    ps1_file = ROOT_DIR / "nunes_fleet_agent.ps1"
    if ps1_file.exists():
        with open(ps1_file, "r", encoding="utf-8") as f:
            ps1_code = f.read()
        ps1_code = re.sub(
            r'https://[a-zA-Z0-9-]+\.trycloudflare\.com',
            tunnel_url,
            ps1_code
        )
        with open(ps1_file, "w", encoding="utf-8") as f:
            f.write(ps1_code)

    # Update nunes_universal_cleaner.py
    py_file = ROOT_DIR / "nunes_universal_cleaner.py"
    if py_file.exists():
        with open(py_file, "r", encoding="utf-8") as f:
            py_code = f.read()
        py_code = re.sub(
            r'https://[a-zA-Z0-9-]+\.trycloudflare\.com',
            tunnel_url,
            py_code
        )
        with open(py_file, "w", encoding="utf-8") as f:
            f.write(py_code)

    # Update index.html and templates
    for h_name in ["index.html", "dashboard/templates/index.html"]:
        h_file = ROOT_DIR / h_name
        if h_file.exists():
            with open(h_file, "r", encoding="utf-8") as f:
                h_code = f.read()
            h_code = re.sub(
                r'https://[a-zA-Z0-9-]+\.trycloudflare\.com',
                tunnel_url,
                h_code
            )
            with open(h_file, "w", encoding="utf-8") as f:
                f.write(h_code)

    # Rebuild dynamic zip
    try:
        from zip_builder import build_client_zip
        build_client_zip(verbose=False)
        print("[OK] Rebuilt dynamic NUNES_FLEET_CLIENT_V7.zip with fresh tunnel URL")
    except Exception as e:
        print(f"[!] Zip build error: {e}")

def deploy_to_vercel():
    print("[*] Promoting update live to Vercel...")
    env = os.environ.copy()
    env["NODE_OPTIONS"] = "--dns-result-order=ipv4first"
    try:
        res = subprocess.run(
            ["cmd.exe", "/c", "vercel deploy --prod --yes"],
            env=env,
            capture_output=True,
            text=True,
            timeout=60
        )
        if res.returncode == 0:
            print("[OK] Vercel edge deployment successful! https://autonomous-system-temp-cleaner-six.vercel.app")
        else:
            print(f"[!] Vercel deploy output: {res.stdout} {res.stderr}")
    except Exception as e:
        print(f"[!] Vercel deploy failed: {e}")

def run_loop():
    while True:
        print("[*] Starting cloudflared tunnel process...")
        proc = subprocess.Popen(
            [CLOUDFLARED_BIN, "tunnel", "--protocol", "http2", "--url", "http://127.0.0.1:8090"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        tunnel_url = None
        start = time.time()
        while time.time() - start < 25:
            line = proc.stderr.readline()
            if not line:
                time.sleep(0.1)
                continue
            if "trycloudflare.com" in line:
                m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
                if m:
                    tunnel_url = m.group(0)
                    break

        if tunnel_url:
            print(f"================================================================")
            print(f"  ACTIVE GLOBAL CLOUDFLARE TUNNEL: {tunnel_url}")
            print(f"================================================================")
            update_vercel_config(tunnel_url)
            update_client_scripts(tunnel_url)
            deploy_to_vercel()
            
            # Keep process monitored
            while proc.poll() is None:
                time.sleep(5)
            print("[!] Tunnel process exited unexpectedly. Restarting in 3 seconds...")
        else:
            print("[!] Could not obtain trycloudflare.com URL. Retrying...")
            try:
                proc.terminate()
            except Exception:
                pass
        time.sleep(3)

if __name__ == "__main__":
    run_loop()
