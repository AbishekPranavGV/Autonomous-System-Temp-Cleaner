import inspect
import sys

with open('dashboard/ai_agent.py', 'r', encoding='utf-8') as f:
    text = f.read()

print("ai_agent.py lines:", len(text.split('\n')))
for l in text.split('\n'):
    if l.strip().startswith('def '):
        print(" ", l.strip())
