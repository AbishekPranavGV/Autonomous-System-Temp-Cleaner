# -*- coding: utf-8 -*-
import sys
import os

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

for fp in ['index.html', 'dashboard/templates/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove misplaced pollLiveFleetStatus from handleQuickAction
    broken_block = """      else if (k === 'audit') refreshDiagnostics();
      pollLiveFleetStatus();
      setInterval(pollLiveFleetStatus, 3000);
      else if (k === 'downloadclient') downloadFreshClientZip();"""

    fixed_block = """      else if (k === 'audit') refreshDiagnostics();
      else if (k === 'downloadclient') downloadFreshClientZip();"""

    if broken_block in content:
        content = content.replace(broken_block, fixed_block)
        print(f"Fixed handleQuickAction in {fp}")

    # Now make sure pollLiveFleetStatus is inside window.addEventListener('DOMContentLoaded', ...)
    dom_target = "updateClock();\n      setInterval(updateClock, 1000);"
    if dom_target in content and "pollLiveFleetStatus();" not in content[content.find(dom_target):content.find(dom_target)+300]:
        content = content.replace(
            dom_target,
            dom_target + "\n      pollLiveFleetStatus();\n      setInterval(pollLiveFleetStatus, 3000);"
        )
        print(f"Placed pollLiveFleetStatus properly in DOMContentLoaded in {fp}")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
