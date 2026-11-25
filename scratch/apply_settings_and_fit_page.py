import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update body and app-window classes to fit into the page without huge gaps
old_body = '<body class="font-sans antialiased min-h-screen p-2 sm:p-4 lg:p-6 transition-colors duration-300">'
new_body = '<body class="font-sans antialiased min-h-screen p-1 sm:p-2 md:p-2.5 transition-colors duration-300">'

old_app_window = '<div class="max-w-[1440px] mx-auto app-window rounded-3xl p-5 sm:p-7 space-y-6 transition-all duration-300">'
new_app_window = '<div class="w-full max-w-[99%] 2xl:max-w-[1680px] mx-auto app-window rounded-2xl sm:rounded-3xl p-3 sm:p-4 md:p-5 space-y-3 sm:space-y-3.5 transition-all duration-300">'

if old_body in content:
    content = content.replace(old_body, new_body, 1)
else:
    print('Warning: old_body not found!')

if old_app_window in content:
    content = content.replace(old_app_window, new_app_window, 1)
else:
    print('Warning: old_app_window not found!')

# 2. Update Header block
header_start = '    <!-- Top Header & Enterprise Command Center -->'
header_end = '    </header>'

h_start = content.find(header_start)
h_end = content.find(header_end, h_start) + len(header_end)

if h_start == -1 or h_end == -1:
    print('Error: Could not find header block!')
    exit(1)

new_header = '''    <!-- Top Header Bar with Top-Right Settings & Aligned Actions -->
    <header class="flex flex-col xl:flex-row items-start xl:items-center justify-between gap-3 pb-2.5 border-b border-slate-200/80 dark:border-white/5">
      
      <!-- Brand & Telemetry Monitor Area (Left) -->
      <div class="space-y-1.5">
        
        <!-- Brand Title & Badges -->
        <div class="flex flex-wrap items-center gap-2.5 sm:gap-3">
          <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-2xl bg-gradient-to-tr from-violet-600 via-indigo-600 to-purple-600 flex items-center justify-center shadow-md shadow-violet-500/25 text-white font-black text-lg select-none flex-shrink-0 animate-pulse">
            ⚡
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <h1 class="text-xl sm:text-2xl font-black tracking-tight text-slate-900 dark:text-white">
              Temp File Remover
            </h1>
            <span class="text-[11px] px-2 py-0.5 rounded-full font-bold bg-violet-100 dark:bg-violet-950/60 text-violet-700 dark:text-violet-300 border border-violet-200 dark:border-violet-800 shadow-sm whitespace-nowrap">
              Mica Light & Obsidian Suite
            </span>
            <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold subtle-pill">
              <span class="w-2 h-2 rounded-full bg-emerald-500 pulse-dot-green"></span>
              <span class="text-slate-700 dark:text-slate-300">tempfileremover.com</span>
              <span class="text-[10px] text-slate-400 dark:text-slate-500">• NUNES Fleet v8.5.0 Quantum</span>
            </div>
          </div>
        </div>

        <!-- Telemetry Status Chips (Compact horizontal strip) -->
        <div class="flex flex-wrap items-center gap-1.5 text-[11px]">
          <!-- Administrator Badge -->
          <div class="px-2.5 py-0.5 rounded-full font-semibold subtle-pill flex items-center gap-1.5" id="adminBadge">
            <span class="text-blue-500 font-bold">🛡️</span>
            <span>Administrator access detected</span>
          </div>

          <!-- License Activated Badge -->
          <div class="px-2.5 py-0.5 rounded-full font-bold bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-500/50 flex items-center gap-1.5 shadow-sm shadow-emerald-500/10">
            <div class="pulse-dot-green"></div>
            <span>License activated</span>
          </div>

          <!-- 4-Hour Loop Active Badge -->
          <div class="px-2.5 py-0.5 rounded-full font-mono text-[10px] font-semibold bg-slate-100 dark:bg-slate-800/60 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-white/5 flex items-center gap-1.5">
            <span>⏰ 4H Loop:</span>
            <span id="nextLoopClock" class="text-violet-600 dark:text-violet-400 font-bold">03h:35m</span>
          </div>

          <!-- Scan Status Badge -->
          <div class="px-2.5 py-0.5 rounded-full font-medium subtle-pill flex items-center gap-1.5" id="scanStatusBadge">
            <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
            <span id="scanStatusText">No scan yet</span>
          </div>
        </div>

      </div>

      <!-- Header Operational Actions & Top-Right Settings Menu (Right) -->
      <div class="flex flex-wrap items-center gap-2 w-full xl:w-auto justify-end">
        
        <!-- Scan selected -->
        <button onclick="triggerScanSelected()" id="btnScanSelected" class="px-3.5 py-1.5 rounded-xl text-xs font-bold subtle-pill border-violet-300 hover:border-violet-400 dark:border-violet-600/50 text-violet-700 dark:text-violet-300 transition-all flex items-center gap-1.5 active:scale-95 shadow-sm" title="Scan selected categories">
          <span>🔍</span>
          <span>Scan selected</span>
        </button>

        <!-- Clean selected (Prominent Primary Action) -->
        <button onclick="triggerCleanSelected()" id="btnCleanSelected" class="px-4.5 py-1.5 rounded-xl text-xs font-black uppercase tracking-wider primary-btn transition-all flex items-center gap-2 active:scale-95 shadow-md shadow-violet-500/30" title="Safely clean junk files">
          <span>⚡</span>
          <span>CLEAN SELECTED</span>
        </button>

        <!-- Anti-Hang Rescue Button -->
        <button onclick="triggerAntiHangRescue()" id="btnAntiHang" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold uppercase bg-rose-50 hover:bg-rose-100 dark:bg-rose-950/40 dark:hover:bg-rose-900/50 text-rose-700 dark:text-rose-400 border border-rose-300 dark:border-rose-700/50 transition-all flex items-center gap-1.5 active:scale-95 shadow-sm" title="Emergency RAM Trim & Frozen Process Resolver">
          <span>🚨</span>
          <span>RESCUE PC</span>
        </button>

        <!-- Cancel / Reset Selection -->
        <button onclick="resetSelection()" class="px-2.5 py-1.5 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-all" title="Reset category selection">
          Cancel
        </button>

        <!-- ⚙️ TOP RIGHT SETTINGS BUTTON WITH CONTENTS FROM IMAGE 1 -->
        <div class="relative" id="settingsContainer">
          <button onclick="toggleSettingsMenu(event)" id="btnTopSettings" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white dark:bg-white dark:hover:bg-slate-100 dark:text-slate-900 shadow-md transition-all flex items-center gap-1.5 active:scale-95" title="Settings & Utilities (Dark Theme, Dashboard, Live Files, Client Download, Updates)">
            <span class="text-sm">⚙️</span>
            <span>Settings</span>
            <span class="text-[9px] opacity-70 transition-transform duration-200" id="settingsArrow">▼</span>
          </button>

          <!-- Settings Dropdown Flyout Panel -->
          <div id="settingsDropdownMenu" class="hidden absolute right-0 mt-2 w-72 sm:w-80 rounded-2xl bg-white/95 dark:bg-[#161324]/95 backdrop-blur-xl border border-slate-200 dark:border-white/10 shadow-2xl z-50 p-3 space-y-2.5 transition-all duration-200">
            
            <!-- Dropdown Title Bar -->
            <div class="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-white/5 px-1">
              <div class="flex items-center gap-1.5">
                <span class="text-sm">⚙️</span>
                <span class="text-xs font-extrabold text-slate-900 dark:text-white uppercase tracking-wider">System Settings</span>
              </div>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-violet-100 dark:bg-violet-950/60 text-violet-700 dark:text-violet-300 font-bold">Quantum v8.5.0</span>
            </div>

            <!-- Image 1 Contents: Theme, Dashboard, Live Files, Download, Updates -->
            <div class="space-y-1 text-xs">
              
              <!-- 🌙 Dark Theme / Light Theme Toggle -->
              <button onclick="toggleTheme()" id="themeToggleBtn" class="w-full px-3 py-2 rounded-xl flex items-center justify-between hover:bg-slate-100 dark:hover:bg-white/5 transition-all font-semibold text-slate-700 dark:text-slate-200" title="Toggle Light / Dark Theme">
                <div class="flex items-center gap-2">
                  <span id="themeIcon">🌙</span>
                  <span id="themeText">Dark Theme</span>
                </div>
                <span class="text-[10px] text-slate-400 font-mono">Appearance</span>
              </button>

              <!-- 📊 Dashboard Button -->
              <button onclick="scrollToDashboard(); toggleSettingsMenu();" id="btnNavDashboard" class="w-full px-3 py-2 rounded-xl flex items-center justify-between hover:bg-violet-50 dark:hover:bg-violet-950/40 text-violet-700 dark:text-violet-300 font-semibold transition-all" title="Jump to Dashboard & Fleet Operations">
                <div class="flex items-center gap-2">
                  <span>📊</span>
                  <span>Dashboard & Fleet Charts</span>
                </div>
                <span class="text-[10px] font-mono">Jump</span>
              </button>

              <!-- 📁 Live Files Button -->
              <button onclick="scrollToLiveFiles(); toggleSettingsMenu();" id="btnNavLiveFiles" class="w-full px-3 py-2 rounded-xl flex items-center justify-between hover:bg-slate-100 dark:hover:bg-white/5 transition-all font-semibold text-slate-700 dark:text-slate-200" title="View Real-Time Monitored & Connected Files">
                <div class="flex items-center gap-2">
                  <span>📁</span>
                  <span>Live Files Monitored</span>
                </div>
                <span id="navLiveFilesCount" class="px-2 py-0.5 rounded-full text-[10px] font-mono bg-violet-100 dark:bg-violet-900/60 text-violet-800 dark:text-violet-300 font-bold">0</span>
              </button>

              <!-- 📥 Download Client (.zip) -->
              <a href="NUNES_FLEET_CLIENT_V7.zip" onclick="downloadFreshClientZip(event); toggleSettingsMenu();" class="w-full px-3 py-2 rounded-xl flex items-center justify-between bg-violet-600 hover:bg-violet-700 text-white font-bold transition-all shadow-sm" title="Download 1-Click Client ZIP for any Windows PC">
                <div class="flex items-center gap-2">
                  <span>📥</span>
                  <span>Download Client (.zip)</span>
                </div>
                <span class="text-[10px] font-mono bg-white/20 px-1.5 py-0.5 rounded">ZIP</span>
              </a>

              <!-- 🔄 Check for updates -->
              <button onclick="checkForUpdates(); toggleSettingsMenu();" class="w-full px-3 py-2 rounded-xl flex items-center justify-between hover:bg-slate-100 dark:hover:bg-white/5 transition-all font-semibold text-slate-700 dark:text-slate-200" title="Check for updates">
                <div class="flex items-center gap-2">
                  <span>🔄</span>
                  <span>Check for updates</span>
                </div>
                <span class="text-[10px] text-emerald-500 font-bold">OTA</span>
              </button>

              <!-- 🤖 Fleet AI Copilot -->
              <button onclick="openAIChatModal(); toggleSettingsMenu();" class="w-full px-3 py-2 rounded-xl flex items-center justify-between hover:bg-slate-100 dark:hover:bg-white/5 transition-all font-semibold text-slate-700 dark:text-slate-200" title="Open Fleet AI Copilot">
                <div class="flex items-center gap-2">
                  <span>🤖</span>
                  <span>Fleet AI Copilot</span>
                </div>
                <span class="text-[10px] text-violet-500 font-bold">Open</span>
              </button>

            </div>

            <!-- Operations Cluster inside Settings Menu -->
            <div class="pt-2 border-t border-slate-100 dark:border-white/5 space-y-1.5">
              <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider px-1">Quick Operations</div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="triggerScanSelected(); toggleSettingsMenu();" class="w-full py-1.5 px-2 rounded-lg text-[11px] font-bold subtle-pill text-violet-700 dark:text-violet-300 flex items-center justify-center gap-1">
                  <span>🔍</span> Scan
                </button>
                <button onclick="triggerCleanSelected(); toggleSettingsMenu();" class="w-full py-1.5 px-2 rounded-lg text-[11px] font-black uppercase primary-btn flex items-center justify-center gap-1 shadow-sm">
                  <span>⚡</span> Clean
                </button>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="triggerAntiHangRescue(); toggleSettingsMenu();" class="w-full py-1.5 px-2 rounded-lg text-[11px] font-bold bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-400 border border-rose-300 dark:border-rose-800 flex items-center justify-center gap-1">
                  <span>🚨</span> Rescue PC
                </button>
                <button onclick="resetSelection(); toggleSettingsMenu();" class="w-full py-1.5 px-2 rounded-lg text-[11px] font-medium text-slate-400 hover:text-slate-700 dark:hover:text-slate-200">
                  Cancel
                </button>
              </div>
            </div>

          </div>
        </div>

      </div>

    </header>'''

content = content[:h_start] + new_header + content[h_end:]

# 3. Tighten the 3-column grid gap
old_grid = '<div class="grid grid-cols-1 lg:grid-cols-12 gap-5 sm:gap-6 items-start">'
new_grid = '<div class="grid grid-cols-1 lg:grid-cols-12 gap-3.5 sm:gap-4 items-start">'
if old_grid in content:
    content = content.replace(old_grid, new_grid, 1)

# 4. Add JavaScript for toggleSettingsMenu and click-outside handler
js_marker = '// ==========================================\n    // TOAST & LOG UTILITIES'
settings_js = '''// ==========================================
    // SETTINGS DROPDOWN & MENU LOGIC
    // ==========================================
    function toggleSettingsMenu(e) {
      if (e) {
        e.stopPropagation();
      }
      const menu = document.getElementById('settingsDropdownMenu');
      const arrow = document.getElementById('settingsArrow');
      if (!menu) return;
      const isHidden = menu.classList.contains('hidden');
      if (isHidden) {
        menu.classList.remove('hidden');
        if (arrow) arrow.style.transform = 'rotate(180deg)';
      } else {
        menu.classList.add('hidden');
        if (arrow) arrow.style.transform = 'rotate(0deg)';
      }
    }

    document.addEventListener('click', function(e) {
      const container = document.getElementById('settingsContainer');
      const menu = document.getElementById('settingsDropdownMenu');
      const arrow = document.getElementById('settingsArrow');
      if (container && !container.contains(e.target)) {
        if (menu && !menu.classList.contains('hidden')) {
          menu.classList.add('hidden');
          if (arrow) arrow.style.transform = 'rotate(0deg)';
        }
      }
    });

    '''

if js_marker in content:
    content = content.replace(js_marker, settings_js + js_marker, 1)
else:
    # Alternative marker
    js_marker2 = 'function showToast('
    content = content.replace(js_marker2, settings_js + js_marker2, 1)

# Write to both index.html and dashboard/templates/index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('dashboard/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully applied settings button and tightened page gaps!')
