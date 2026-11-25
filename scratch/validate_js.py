import subprocess
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract script blocks
scripts = re.findall(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>', html)
print(f"Found {len(scripts)} inline script blocks.")

for i, s in enumerate(scripts, 1):
    # Test with node vm
    test_js = f"""
    const vm = require('vm');
    const code = {repr(s)};
    try {{
      new vm.Script(code);
      console.log('Script block {i}: SYNTAX VALID');
    }} catch (e) {{
      console.error('Script block {i} ERROR:', e.message);
      process.exit(1);
    }}
    """
    res = subprocess.run(["node", "-e", test_js], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED on block {i}:", res.stderr)
        sys.exit(1)
    else:
        print(res.stdout.strip())

print("All inline scripts in index.html are 100% syntactically valid!")
