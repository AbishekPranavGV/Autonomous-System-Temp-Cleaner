import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Part 1: Remove the 7 UI texts from header
old_brand_start = '      <!-- Brand & Telemetry Monitor Area (Left) -->'
old_brand_end = '      <!-- Header Operational Actions & Top-Right Settings Menu (Right) -->'

b_start = html.find(old_brand_start)
b_end = html.find(old_brand_end, b_start)

if b_start == -1 or b_end == -1:
    print('Error: Could not find brand area in index.html!')
    exit(1)

new_brand = '''      <!-- Brand Area (Clean Minimalist Title) -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-violet-600 via-indigo-600 to-purple-600 flex items-center justify-center shadow-md shadow-violet-500/25 text-white font-black text-lg select-none flex-shrink-0 animate-pulse">
          ⚡
        </div>
        <h1 class="text-xl sm:text-2xl font-black tracking-tight text-slate-900 dark:text-white">
          Temp File Remover
        </h1>
        <!-- Hidden containers to maintain JS element ID safety without any UI text -->
        <span id="adminBadge" class="hidden"></span>
        <span id="scanStatusBadge" class="hidden"><span id="scanStatusText"></span></span>
        <span id="nextLoopClock" class="hidden"></span>
      </div>

'''

html = html[:b_start] + new_brand + html[b_end:]

# Part 2: Update AI welcome greeting to friendly 1-sentence informal speech
old_welcome_start = '        <!-- Initial Welcome Message from AI -->'
old_welcome_end = '      </div>\n\n      <!-- Quick Action Prompt Pills (Horizontal Scroll) -->'

w_start = html.find(old_welcome_start)
w_end = html.find(old_welcome_end, w_start)

if w_start == -1 or w_end == -1:
    print('Error: Could not find AI welcome block in index.html!')
    exit(1)

new_welcome = '''        <!-- Initial Welcome Message from AI (Friendly & Informal in 1 Sentence) -->
        <div class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-violet-600 via-indigo-600 to-purple-600 text-white flex items-center justify-center text-sm shrink-0 shadow-md">
            🤖
          </div>
          <div class="p-3.5 rounded-2xl rounded-tl-sm bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-white/10 text-slate-800 dark:text-slate-200 shadow-sm max-w-[90%] space-y-2">
            <div class="chat-bubble-text text-xs leading-relaxed font-medium">
              Hey there! I'm watching over your computers to keep them running super fast and clutter-free, so what can I clean or speed up for you today?
            </div>
            <div class="pt-1 flex flex-wrap gap-1.5">
              <button onclick="sendQuickPrompt('audit')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-violet-50 hover:bg-violet-100 dark:bg-violet-950/60 dark:hover:bg-violet-900/60 text-violet-700 dark:text-violet-300 border border-violet-200 dark:border-violet-800 transition-all flex items-center gap-1 active:scale-95">
                <span>🛡️ 100% Accuracy Audit</span>
              </button>
              <button onclick="sendQuickPrompt('clean')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-950/60 dark:hover:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 transition-all flex items-center gap-1 active:scale-95">
                <span>⚡ Safe Clean Fleet</span>
              </button>
            </div>
          </div>
        </div>
'''

html = html[:w_start] + new_welcome + html[w_end:]

# Update clearAIChatHistory in JS
old_clear_marker = 'Session refreshed. 100,000x Neural Sentry ready for diagnostics.'
new_clear_text = "Hey there! I'm watching over your computers to keep them running super fast and clutter-free, so what can I clean or speed up for you today?"
html = html.replace(old_clear_marker, new_clear_text)

# Update generateAutonomousAiReply fallback in JS
old_fallback_start = '// Default fallback\n      return {'
old_fallback_marker = 'reply: `### ⚡ Fluxyn Neural Operations Sentry\\n\\nTargeting **${node}**.\\n\\nSelect an action below or ask me to:\\n- 🛡️ Run an **Accuracy Audit**\\n- ⚡ **Safe Clean** temporary caches\\n- 🚨 **Flush RAM** to resolve system hangs\\n- 💻 **Connect any computer** via client ZIP`,'
new_fallback_marker = 'reply: "Hey there! I\'m watching over your computers to keep them running super fast and clutter-free, so what can I clean or speed up for you today?",'
html = html.replace(old_fallback_marker, new_fallback_marker)

# Write to index.html and dashboard/templates/index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('dashboard/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated index.html and dashboard/templates/index.html!')

# 2. Update dashboard/ai_agent.py
with open('dashboard/ai_agent.py', 'r', encoding='utf-8') as f:
    agent_code = f.read()

old_agent_greeting_start = '        # Default Intelligent Assistant Response\n        reply = ('
agent_idx = agent_code.find(old_agent_greeting_start)
if agent_idx != -1:
    agent_end = agent_code.find('action = {"type": "GENERAL_HELP"}', agent_idx)
    new_agent_greeting = '''        # Default Intelligent Assistant Response (Friendly 1-Sentence Informal Speech)
        reply = (
            "Hey there! I'm watching over your computers to keep them running super fast and clutter-free, so what can I clean or speed up for you today?"
        )
        '''
    agent_code = agent_code[:agent_idx] + new_agent_greeting + agent_code[agent_end:]
    with open('dashboard/ai_agent.py', 'w', encoding='utf-8') as f:
        f.write(agent_code)
    print('Updated dashboard/ai_agent.py!')
else:
    print('Warning: Default assistant response block not found in ai_agent.py!')
