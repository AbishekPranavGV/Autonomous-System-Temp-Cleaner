# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

for f in ['CONNECT_THIS_PC.bat', 'CONNECT_FLEET_PC.bat', 'INSTALL_4H_SERVICE.bat', 'zip_builder.py']:
    print(f"=== {f} ===")
    try:
        with open(f, 'r', encoding='utf-8') as fl:
            print(fl.read()[:800])
    except Exception as e:
        print(f"Error reading {f}: {e}")
