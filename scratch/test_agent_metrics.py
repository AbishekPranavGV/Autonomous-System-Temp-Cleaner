import os
import sys
import platform
import subprocess
import json

sys.stdout.reconfigure(encoding='utf-8')

print("OS:", platform.platform())

# Test top processes
try:
    cmd = 'tasklist /FO CSV /NH'
    out = subprocess.check_output(cmd, shell=True, text=True, timeout=3)
    procs = []
    for line in out.strip().splitlines()[:15]:
        parts = [p.strip('"') for p in line.split('","')]
        if len(parts) >= 5:
            procs.append({"name": parts[0], "pid": parts[1], "mem": parts[4]})
    print("Found top procs:", len(procs), procs[:3])
except Exception as e:
    print("Error listing procs:", e)
