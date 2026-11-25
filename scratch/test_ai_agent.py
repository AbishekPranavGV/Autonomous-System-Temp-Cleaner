import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding='utf-8')

from dashboard.ai_agent import FleetAIAgent

agent = FleetAIAgent()
hw = agent.get_hardware_telemetry()
print("HW telemetry loaded:", {k: v for k, v in hw.items() if k not in ['top_processes']})

res_en = agent.process_message("Why is my computer slow?")
print("English reply (length):", len(res_en['reply']), "Risk:", res_en['risk'])

res_ta = agent.process_message("கணினி ஏன் மெதுவாக உள்ளது?")
print("Tamil reply (length):", len(res_ta['reply']), "Risk:", res_ta['risk'])
print("Tamil preview:", res_ta['reply'][:120])
