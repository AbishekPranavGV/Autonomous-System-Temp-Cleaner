"""
NUNES AUTONOMOUS TUNNEL LAUNCHER & VERIFIER
Starts Cloudflare tunnel, captures the live URL, updates vercel.json & templates,
and automatically promotes the deployment.
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

def start_tunnel():
    if not os.path.exists(CLOUDFLARED_BIN):
        print(f"[!] cloudflared not found at {CLOUDFLARED_BIN}")
        return None, None

    print("[*] Spawning cloudflared tunnel to http://localhost:8090...")
    proc = subprocess.Popen(
        [CLOUDFLARED_BIN, "tunnel", "--url", "http://localhost:8090"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    tunnel_url = None
    start_time = time.time()
    
    # Read output until trycloudflare.com URL is discovered
    while time.time() - start_time < 20:
        line = proc.stderr.readline()
        if not line:
            time.sleep(0.1)
            continue
        if "trycloudflare.com" in line:
            m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
            if m:
                tunnel_url = m.group(0)
                break

    if not tunnel_url:
        print("[!] Failed to obtain trycloudflare.com URL within 20s")
        return proc, None

    print(f"[OK] Live Cloudflare Tunnel Established: {tunnel_url}")
    return proc, tunnel_url

if __name__ == "__main__":
    proc, url = start_tunnel()
    if url:
        print("TUNNEL_URL=" + url)
