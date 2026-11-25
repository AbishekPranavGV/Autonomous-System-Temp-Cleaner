import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

test_file = Path(os.environ.get('TEMP', 'C:/Windows/Temp')) / '__latency_probe.tmp'
try:
    t0 = time.perf_counter()
    with open(test_file, 'wb') as f:
        f.write(b'0' * 4096)
        f.flush()
        os.fsync(f.fileno())
    t1 = time.perf_counter()
    with open(test_file, 'rb') as f:
        _ = f.read()
    t2 = time.perf_counter()
    test_file.unlink(missing_ok=True)
    write_ms = round((t1 - t0) * 1000, 2)
    read_ms = round((t2 - t1) * 1000, 2)
    total_ms = round((t2 - t0) * 1000, 2)
    print(f"Live Disk Latency: {total_ms} ms (write: {write_ms} ms, read: {read_ms} ms)")
except Exception as e:
    print("Error measuring latency:", e)
