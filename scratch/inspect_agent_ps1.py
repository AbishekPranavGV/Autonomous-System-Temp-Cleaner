# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

print("File length:", len(text))

# Search for URLs or endpoints
urls = re.findall(r'https?://[^\s"\'`)]+', text)
print("URLs found in nunes_fleet_agent.ps1:")
for u in set(urls):
    print(" -", u)

# Search for param or config variables at top
print("\nFirst 80 lines:")
lines = text.splitlines()
for i in range(min(80, len(lines))):
    print(f"{i+1}: {lines[i]}")
