import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all occurrences of 35-day or 35 in HTML text
matches = re.findall(r'.{0,40}35[ -]?[Dd]ay.{0,40}', html)
for m in matches:
    print("35 match:", m.strip())

print("\n--- Version occurrences ---")
v_matches = re.findall(r'.{0,30}8\.5\.0.{0,30}', html)
for v in v_matches[:10]:
    print("Version match:", v.strip())
