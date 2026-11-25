# -*- coding: utf-8 -*-
import os
from pathlib import Path

for p in [
    Path('dashboard/data/status/TEST-REMOTE-LAPTOP.status'),
    Path('dashboard/data/results/TEST-REMOTE-LAPTOP.result'),
    Path('dashboard/data/requests/TEST-REMOTE-LAPTOP.request'),
    Path('dashboard/data/queues/TEST-REMOTE-LAPTOP.json')
]:
    if p.exists():
        p.unlink()
        print(f"Removed {p}")

# Rescan local fleet
import sys
sys.path.insert(0, str(Path('dashboard').resolve()))
import app
app.CACHED_SCAN_DATA = app.scan_local_fleet()
print("Rescanned local fleet successfully. Total monitored:", app.CACHED_SCAN_DATA.get('total_monitored'))
