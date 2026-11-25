import re

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the old header block to be replaced
old_header_start = '    <!-- Top Header Bar -->'
old_header_end = '    </header>'

start_idx = content.find(old_header_start)
end_idx = content.find(old_header_end, start_idx) + len(old_header_end)

if start_idx == -1 or end_idx == -1:
    print('Error: Could not find header block!')
    exit(1)

old_header = content[start_idx:end_idx]

new_header = '''    <!-- Top Header & Enterprise Command Center -->
    <header class="space-y-3.5 pb-2 border-b border-slate-200/80 dark:border-white/5">

      <!-- TOP COLUMN TIER 1: Brand & Global Navigation -->
      <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
        
        <!-- Brand & Title Area -->
        <div class="flex items-center gap-3.5">
          <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-violet-600 via-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-violet-500/25 text-white font-black text-xl select-none flex-shrink-0 animate-pulse">
            ⚡
          </div>
          <div>
            <div class="flex flex-wrap items-center gap-2 sm:gap-2.5">
              <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">
                Temp File Remover
              </h1>
              <span class="text-xs px-2.5 py-0.5 rounded-full font-bold bg-violet-100 dark:bg-violet-950/60 text-violet-700 dark:text-violet-300 border border-violet-200 dark:border-violet-800 shadow-sm whitespace-nowrap">
                Mica Light & Obsidian Suite
              </span>
            </div>
            <div class="flex flex-wrap items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mt-1">
              <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold subtle-pill">
                <span class="w-2 h-2 rounded-full bg-emerald-500 pulse-dot-green"></span>
                <span class="text-slate-700 dark:text-slate-300">tempfileremover.com</span>
                <span class="text-[10px] text-slate-400 dark:text-slate-500">• NUNES Fleet v8.5.0 Quantum Edition</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Tier 1 Global Navigation & System Tools -->
        <div class="flex flex-wrap items-center gap-2 sm:gap-2.5 w-full lg:w-auto justify-start lg:justify-end">
          
          <!-- Fleet AI Copilot Pill (LeadAuto Style) -->
          <button onclick="openAIChatModal()" class="px-3.5 py-2 rounded-full text-xs font-bold bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white shadow-md shadow-violet-500/20 transition-all flex items-center gap-1.5 active:scale-95" title="Open Fleet AI Copilot Assistant">
            <span>🤖</span>
            <span>AI Copilot</span>
          </button>

          <!-- Theme Toggle (Light / Dark) -->
          <button onclick="toggleTheme()" id="themeToggleBtn" class="px-3.5 py-2 rounded-full text-xs font-semibold subtle-pill transition-all flex items-center gap-1.5 active:scale-95" title="Toggle Light / Dark Theme">
            <span id="themeIcon">🌙</span>
            <span id="themeText">Dark Theme</span>
          </button>

          <!-- Dashboard Button -->
          <button onclick="scrollToDashboard()" id="btnNavDashboard" class="px-3.5 py-2 rounded-full text-xs font-bold bg-violet-100 hover:bg-violet-200 text-violet-800 dark:bg-violet-950/70 dark:hover:bg-violet-900/80 dark:text-violet-300 border border-violet-300 dark:border-violet-700/60 transition-all flex items-center gap-1.5 active:scale-95 shadow-sm" title="Jump to Dashboard & Fleet Operations">
            <span>📊</span>
            <span>Dashboard</span>
          </button>

          <!-- Live Files Button -->
          <button onclick="scrollToLiveFiles()" id="btnNavLiveFiles" class="px-3.5 py-2 rounded-full text-xs font-semibold subtle-pill transition-all flex items-center gap-1.5 active:scale-95" title="View Real-Time Monitored & Connected Files">
            <span>📁</span>
            <span>Live Files</span>
            <span id="navLiveFilesCount" class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-violet-200/80 dark:bg-violet-900/80 text-violet-800 dark:text-violet-200">0</span>
          </button>

          <!-- Download Fleet Client ZIP (Prominent Pill) -->
          <a href="NUNES_FLEET_CLIENT_V7.zip" onclick="downloadFreshClientZip(event)" class="px-4 py-2 rounded-full text-xs font-bold bg-slate-800 hover:bg-slate-900 dark:bg-slate-700 dark:hover:bg-slate-600 text-white shadow-sm transition-all flex items-center gap-1.5 active:scale-95 whitespace-nowrap" title="Download 1-Click Client ZIP for any Windows PC">
            <span>📥</span>
            <span>Download Client (.zip)</span>
          </a>

          <!-- Check for updates -->
          <button onclick="checkForUpdates()" class="px-3.5 py-2 rounded-full text-xs font-semibold subtle-pill text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all active:scale-95">
            Check for updates
          </button>

        </div>

      </div>

      <!-- TOP COLUMN TIER 2: Enterprise Command Ribbon & Execution Matrix -->
      <div class="surface-card rounded-2xl p-2.5 sm:px-4 sm:py-3 border border-slate-200/90 dark:border-white/10 shadow-sm flex flex-col xl:flex-row items-stretch xl:items-center justify-between gap-3.5">
        
        <!-- Left Side: Live System Health & Telemetry Badges -->
        <div class="flex flex-wrap items-center gap-2 text-xs">
          <!-- Administrator Badge -->
          <div class="px-3 py-1.5 rounded-xl font-semibold subtle-pill flex items-center gap-1.5" id="adminBadge">
            <span class="text-blue-500 font-bold">🛡️</span>
            <span>Administrator access detected</span>
          </div>

          <!-- License / Fleet Verified Badge -->
          <div class="px-3 py-1.5 rounded-xl font-bold bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-500/50 flex items-center gap-1.5 shadow-sm shadow-emerald-500/10">
            <div class="pulse-dot-green"></div>
            <span>License activated</span>
          </div>

          <!-- 4-Hour Loop Live Badge -->
          <div class="px-3 py-1.5 rounded-xl font-mono text-[11px] font-semibold bg-slate-100 dark:bg-slate-800/60 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-white/5 flex items-center gap-1.5">
            <span>⏰ 4H Loop Active:</span>
            <span id="nextLoopClock" class="text-violet-600 dark:text-violet-400 font-bold">03h:42m</span>
          </div>

          <!-- Scan Status Badge -->
          <div class="px-3 py-1.5 rounded-xl font-semibold subtle-pill flex items-center gap-1.5" id="scanStatusBadge">
            <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
            <span id="scanStatusText">No scan yet</span>
          </div>
        </div>

        <!-- Right Side: Unified Primary Action Command Cluster -->
        <div class="flex flex-wrap items-center gap-2 justify-end sm:justify-start xl:justify-end">
          <!-- Scan selected -->
          <button onclick="triggerScanSelected()" id="btnScanSelected" class="px-4 py-2 rounded-xl text-xs font-bold subtle-pill border-violet-300 hover:border-violet-400 dark:border-violet-600/50 text-violet-700 dark:text-violet-300 transition-all flex items-center gap-1.5 active:scale-95 shadow-sm">
            <span>🔍</span>
            <span>Scan selected</span>
          </button>

          <!-- Clean selected (Prominent Call to Action) -->
          <button onclick="triggerCleanSelected()" id="btnCleanSelected" class="px-5 py-2 rounded-xl text-xs font-black uppercase tracking-wider primary-btn transition-all flex items-center gap-2 active:scale-95 shadow-md shadow-violet-500/30">
            <span>⚡</span>
            <span>CLEAN SELECTED</span>
          </button>

          <!-- Anti-Hang Rescue Button -->
          <button onclick="triggerAntiHangRescue()" id="btnAntiHang" class="px-4 py-2 rounded-xl text-xs font-extrabold uppercase bg-rose-50 hover:bg-rose-100 dark:bg-rose-950/40 dark:hover:bg-rose-900/50 text-rose-700 dark:text-rose-400 border border-rose-300 dark:border-rose-700/50 transition-all flex items-center gap-1.5 active:scale-95 shadow-sm" title="Emergency RAM Trim & Frozen Process Resolver">
            <span>🚨</span>
            <span>RESCUE PC</span>
          </button>

          <!-- Cancel -->
          <button onclick="resetSelection()" class="px-3.5 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-all">
            Cancel
          </button>
        </div>

      </div>

    </header>'''

# Also add Side Column Fast Action Console right after overview card
overview_end_marker = '        <!-- Card: Safety / Controlled Cleanup -->'
if overview_end_marker not in content:
    print('Error: Could not find Safety card marker!')
    exit(1)

side_console = '''        <!-- Card: Fast Action Console (Side Column Quick Access) -->
        <div class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 border border-violet-200/60 dark:border-violet-900/40">
          <div class="flex items-center justify-between text-xs font-bold text-slate-400 uppercase tracking-wider">
            <span class="flex items-center gap-1.5 text-violet-700 dark:text-violet-300">
              <span>⚡</span> Fast Action Console
            </span>
            <span class="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono font-bold">Ready</span>
          </div>
          
          <div class="space-y-2 pt-1">
            <button onclick="triggerCleanSelected()" class="w-full py-2.5 px-3 rounded-xl text-xs font-black uppercase tracking-wider primary-btn flex items-center justify-center gap-2 shadow-md shadow-violet-500/20 active:scale-95 transition-all">
              <span>⚡</span> Clean Selected Now
            </button>
            <div class="grid grid-cols-2 gap-2">
              <button onclick="triggerScanSelected()" class="w-full py-2 px-2.5 rounded-xl text-xs font-bold subtle-pill border-violet-300 hover:border-violet-400 dark:border-violet-700/60 text-violet-700 dark:text-violet-300 flex items-center justify-center gap-1.5 active:scale-95 transition-all">
                <span>🔍</span> Scan Now
              </button>
              <button onclick="triggerAntiHangRescue()" class="w-full py-2 px-2.5 rounded-xl text-xs font-bold bg-rose-50 hover:bg-rose-100 dark:bg-rose-950/40 dark:hover:bg-rose-900/50 text-rose-700 dark:text-rose-400 border border-rose-300 dark:border-rose-700/50 flex items-center justify-center gap-1.5 active:scale-95 transition-all">
                <span>🚨</span> Rescue PC
              </button>
            </div>
            <button onclick="openAIChatModal()" class="w-full py-2 px-3 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800/80 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-white/5 flex items-center justify-center gap-2 active:scale-95 transition-all">
              <span>🤖</span> Ask Fleet AI Copilot
            </button>
          </div>
        </div>

'''

new_content = content[:start_idx] + new_header + content[end_idx:]
new_content = new_content.replace(overview_end_marker, side_console + overview_end_marker)

# Write to index.html and dashboard/templates/index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

with open('dashboard/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Successfully updated index.html and dashboard/templates/index.html!')
