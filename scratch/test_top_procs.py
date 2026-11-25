import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

cmd = 'tasklist /FO CSV /NH'
out = subprocess.check_output(cmd, shell=True, text=True, timeout=3)
procs = []
for line in out.strip().splitlines():
    parts = [p.strip('"') for p in line.split('","')]
    if len(parts) >= 5:
        name = parts[0]
        pid = parts[1]
        mem_str = parts[4].replace(',', '').replace(' K', '').strip()
        try:
            mem_kb = int(mem_str)
            mem_mb = round(mem_kb / 1024, 1)
        except ValueError:
            mem_mb = 0
        procs.append({"name": name, "pid": pid, "mem_mb": mem_mb})

procs.sort(key=lambda x: x["mem_mb"], reverse=True)
print("Top 5 RAM processes:")
for p in procs[:5]:
    print(f"  {p['name']} (PID: {p['pid']}): {p['mem_mb']} MB")
