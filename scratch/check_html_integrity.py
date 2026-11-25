# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

for path in ['index.html', 'dashboard/templates/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"=== {path} ===")
    print("Length:", len(content))
    if "'''" in content:
        print("CRITICAL: Found ''' in file!")
    else:
        print("OK: No ''' found.")
    
    # Check if </body> and </html> are at the end
    last_100 = content[-200:]
    print("Tail end:\n" + last_100.strip())
