import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from app import scan_local_fleet, get_config
import requests

def main():
    cfg = get_config()
    v_url = cfg.get('vercel_url', 'https://nunes-temp-cleaner-dashboard.vercel.app').rstrip('/')
    sync_endpoint = v_url + '/api/sync'

    print("Scanning local NAS cleaner shares...")
    data = scan_local_fleet()
    if data:
        print(f"Found {data['total_monitored']} PCs ({data['online_count']} Online).")
        print(f"Pushing update to: {sync_endpoint}")
        headers = {
            'Content-Type': 'application/json',
            'X-Sync-Token': cfg.get('sync_token', 'nunes_temp_cleaner_2026')
        }
        res = requests.post(sync_endpoint, json=data, headers=headers, timeout=10)
        print("Vercel Response:", res.status_code, res.text)
    else:
        print("Could not scan fleet. Check NAS connection.")

if __name__ == '__main__':
    main()
