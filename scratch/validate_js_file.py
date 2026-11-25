import subprocess
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>', html)
print(f"Found {len(scripts)} inline script blocks.")

for i, s in enumerate(scripts, 1):
    tmp_path = f"scratch/test_block_{i}.js"
    with open(tmp_path, "w", encoding="utf-8") as tf:
        tf.write(s)
    
    node_checker = f"""
    const fs = require('fs');
    const vm = require('vm');
    const code = fs.readFileSync('{tmp_path}', 'utf-8');
    try {{
      new vm.Script(code);
      console.log('Script block {i}: SYNTAX VALID');
    }} catch (e) {{
      console.error('Script block {i} SYNTAX ERROR:', e.message);
      process.exit(1);
    }}
    """
    chk_script = f"scratch/runner_{i}.js"
    with open(chk_script, "w", encoding="utf-8") as cf:
        cf.write(node_checker)

    res = subprocess.run(["node", chk_script], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED on block {i}:", res.stderr)
        sys.exit(1)
    else:
        print(res.stdout.strip())

print("All inline scripts in index.html are 100% syntactically valid!")
