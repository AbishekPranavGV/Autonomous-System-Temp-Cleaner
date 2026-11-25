# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

for f in ['tunnel_launcher.py', 'tunnel_service.py']:
    print(f"=== {f} ===")
    try:
        with open(f, 'r', encoding='utf-8') as fl:
            print(fl.read())
    except Exception as e:
        print(f"Error reading {f}: {e}")
