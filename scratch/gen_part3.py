# Part 3: Sections 1, 2, and 3
import sys

sys.stdout.reconfigure(encoding='utf-8')

SECTIONS_1_2_3 = '''
    <!-- ============================================================== -->
    <!-- SECTION 1: OVERVIEW & PERFORMANCE SUMMARIES                   -->
    <!-- ============================================================== -->
    <section id="sec_overview" class="section-view active space-y-4">
      
      <!-- Timeframe Summary Bar (Today / Month / Year) -->
      <div class="flex flex-wrap items-center justify-between gap-3 p-3 surface-card rounded-2xl">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider" data-i18n="timeframe_label">Performance Period:</span>
          <div class="inline-flex p-1 bg-slate-100 dark:bg-slate-800 rounded-xl">
            <button onclick="setTimeframe('today')" id="tfBtn_today" class="px-3 py-1 rounded-lg text-xs font-bold bg-white dark:bg-slate-700 text-sky-700 dark:text-sky-300 shadow-sm transition-all" data-i18n="today">Today</button>
            <button onclick="setTimeframe('month')" id="tfBtn_month" class="px-3 py-1 rounded-lg text-xs font-medium text-slate-600 dark:text-slate-300 hover:text-sky-600 transition-all" data-i18n="month">This Month</button>
            <button onclick="setTimeframe('year')" id="tfBtn_year" class="px-3 py-1 rounded-lg text-xs font-medium text-slate-600 dark:text-slate-300 hover:text-sky-600 transition-all" data-i18n="year">This Year</button>
          </div>
        </div>
        <div class="flex items-center gap-3 text-xs font-mono">
          <span class="text-slate-500 dark:text-slate-400"><span data-i18n="verified_sweeps">Verified Sweeps:</span> <strong class="text-slate-900 dark:text-white" id="tfSweepsCount">18</strong></span>
          <span class="text-slate-300 dark:text-slate-700">|</span>
          <span class="text-slate-500 dark:text-slate-400"><span data-i18n="fleet_health_score">Fleet Health:</span> <strong class="text-emerald-600 dark:text-emerald-400" id="tfHealthScore">99.8%</strong></span>
        </div>
      </div>

      <!-- 4 Key Performance Metric Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        
        <!-- Card 1: Reclaimable Opportunity -->
        <div class="surface-card rounded-2xl p-4 sm:p-5 relative overflow-hidden group">
          <div class="flex items-center justify-between pb-2">
            <span class="text-xs font-bold text-slate-500 dark:text-slate-400" data-i18n="card_reclaimable_title">Potential Recovery</span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-sky-100 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300">REAL-TIME</span>
          </div>
          <div class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight" id="overviewSizeText">1.49 GB</div>
          <div class="mt-2 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
            <span><strong id="overviewFilesText" class="text-slate-700 dark:text-slate-300">920</strong> candidate files</span>
            <span><strong id="overviewCategoriesText" class="text-slate-700 dark:text-slate-300">8</strong> categories</span>
          </div>
        </div>

        <!-- Card 2: Zero-Loss Security Shield -->
        <div class="surface-card rounded-2xl p-4 sm:p-5 relative overflow-hidden group border-emerald-200/80 dark:border-emerald-900/50">
          <div class="flex items-center justify-between pb-2">
            <span class="text-xs font-bold text-slate-500 dark:text-slate-400" data-i18n="card_safety_title">Zero-Loss Protection</span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300">ENFORCED</span>
          </div>
          <div class="text-2xl sm:text-3xl font-black text-emerald-600 dark:text-emerald-400 tracking-tight">100% Locked</div>
          <div class="mt-2 text-xs text-slate-500 dark:text-slate-400" data-i18n="card_safety_sub">
            Downloads, Desktop & Documents strictly excluded
          </div>
        </div>

        <!-- Card 3: Active Fleet Nodes -->
        <div class="surface-card rounded-2xl p-4 sm:p-5 relative overflow-hidden group">
          <div class="flex items-center justify-between pb-2">
            <span class="text-xs font-bold text-slate-500 dark:text-slate-400" data-i18n="card_nodes_title">Active Monitored PCs</span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-indigo-100 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300" id="overviewOnlineBadge">4 ONLINE</span>
          </div>
          <div class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight" id="overviewNodesCount">4 Workstations</div>
          <div class="mt-2 text-xs text-slate-500 dark:text-slate-400 flex items-center justify-between">
            <span data-i18n="grouped_departments">4 Office Departments</span>
            <button onclick="switchTab('fleet')" class="text-sky-600 dark:text-sky-400 hover:underline font-bold text-[11px]" data-i18n="view_fleet">View Fleet →</button>
          </div>
        </div>

        <!-- Card 4: Unified 30-Day Retention -->
        <div class="surface-card rounded-2xl p-4 sm:p-5 relative overflow-hidden group" id="retention30DayContainer">
          <div class="flex items-center justify-between pb-2">
            <span class="text-xs font-bold text-slate-500 dark:text-slate-400" data-i18n="card_retention_title">30-Day Unified Retention</span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-cyan-100 dark:bg-cyan-950/60 text-cyan-700 dark:text-cyan-300">COMPLIANT</span>
          </div>
          <div class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight" id="overviewRetentionBackups">48 Snapshots</div>
          <div class="mt-2 text-xs text-slate-500 dark:text-slate-400 flex items-center justify-between">
            <span>Auto-purged &gt;30 days</span>
            <button onclick="switchTab('settings')" class="text-sky-600 dark:text-sky-400 hover:underline font-bold text-[11px]" data-i18n="settings">Rules →</button>
          </div>
        </div>

      </div>

      <!-- Department Workstations Grid & Live Console Row -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        
        <!-- Fleet Workstations Summary by Department (2 Cols) -->
        <div class="lg:col-span-2 surface-card rounded-2xl p-4 sm:p-5 space-y-3.5">
          <div class="flex items-center justify-between border-b border-sky-100 dark:border-sky-950/60 pb-3">
            <div>
              <h3 class="text-sm font-extrabold text-slate-900 dark:text-white" data-i18n="dept_hub_title">NUNES Office Computers by Department</h3>
              <p class="text-xs text-slate-500 dark:text-slate-400" data-i18n="dept_hub_sub">Live Win32 telemetry, heartbeat freshness & safe remote controls</p>
            </div>
            <button onclick="switchTab('fleet')" class="text-xs font-bold text-sky-600 dark:text-sky-400 hover:underline" data-i18n="manage_all">Manage All PCs →</button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3" id="overviewFleetGrid">
            <!-- Node 1: Engineering & Lab -->
            <div class="p-3 rounded-xl border border-sky-100 dark:border-white/5 bg-sky-50/40 dark:bg-slate-900/40 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-white font-mono">DESKTOP-M378M07</span>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-400">ONLINE (0.1m)</span>
              </div>
              <div class="text-[11px] font-semibold text-sky-700 dark:text-sky-400">Department: Engineering & Lab (Host PC)</div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
                <div class="bg-sky-600 h-1.5 rounded-full" style="width: 91%"></div>
              </div>
              <div class="flex justify-between text-[11px] text-slate-500 dark:text-slate-400 font-mono">
                <span>Free: <strong>10.3 GB</strong></span>
                <span>Used: <strong>91.4%</strong></span>
              </div>
            </div>

            <!-- Node 2: Accounts & Finance -->
            <div class="p-3 rounded-xl border border-sky-100 dark:border-white/5 bg-sky-50/40 dark:bg-slate-900/40 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-white font-mono">DESKTOP-EV2F0TV</span>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-400">ONLINE (1.2m)</span>
              </div>
              <div class="text-[11px] font-semibold text-indigo-700 dark:text-indigo-400">Department: Accounts & Finance</div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
                <div class="bg-indigo-600 h-1.5 rounded-full" style="width: 88%"></div>
              </div>
              <div class="flex justify-between text-[11px] text-slate-500 dark:text-slate-400 font-mono">
                <span>Free: <strong>28.5 GB</strong></span>
                <span>Used: <strong>88.6%</strong></span>
              </div>
            </div>

            <!-- Node 3: Production & Quality -->
            <div class="p-3 rounded-xl border border-sky-100 dark:border-white/5 bg-sky-50/40 dark:bg-slate-900/40 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-white font-mono">DESKTOP-I2MHDIB</span>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-400">ONLINE (3.4m)</span>
              </div>
              <div class="text-[11px] font-semibold text-teal-700 dark:text-teal-400">Department: Production & Quality</div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
                <div class="bg-teal-600 h-1.5 rounded-full" style="width: 82%"></div>
              </div>
              <div class="flex justify-between text-[11px] text-slate-500 dark:text-slate-400 font-mono">
                <span>Free: <strong>42.1 GB</strong></span>
                <span>Used: <strong>82.0%</strong></span>
              </div>
            </div>

            <!-- Node 4: Front Office & Sales -->
            <div class="p-3 rounded-xl border border-sky-100 dark:border-white/5 bg-sky-50/40 dark:bg-slate-900/40 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-white font-mono">DESKTOP-F8G3T2C</span>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-400">ONLINE (4.1m)</span>
              </div>
              <div class="text-[11px] font-semibold text-amber-700 dark:text-amber-400">Department: Front Office & Sales</div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
                <div class="bg-amber-600 h-1.5 rounded-full" style="width: 74%"></div>
              </div>
              <div class="flex justify-between text-[11px] text-slate-500 dark:text-slate-400 font-mono">
                <span>Free: <strong>64.0 GB</strong></span>
                <span>Used: <strong>74.4%</strong></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Terminal Execution Log & Activity Stream (1 Col) -->
        <div class="surface-card rounded-2xl p-4 sm:p-5 flex flex-col justify-between space-y-3">
          <div class="flex items-center justify-between border-b border-sky-100 dark:border-sky-950/60 pb-2">
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white" data-i18n="activity_stream_title">Terminal Stream</h3>
            </div>
            <button onclick="fetchTerminalLogs()" class="text-[10px] text-sky-600 font-mono hover:underline">Refresh</button>
          </div>
          <div class="bg-slate-950 text-slate-200 font-mono text-[11px] p-3 rounded-xl h-48 overflow-y-auto space-y-1.5 border border-slate-800" id="terminalStream">
            <div class="text-sky-400">⚡ [INIT] NUNES AI PC Command Center v10.0 initialized.</div>
            <div class="text-emerald-400">🛡️ [SAFEGUARD] 30-Day Retention & Allowlist rules enforced.</div>
            <div class="text-slate-400">⏰ [LOOP] 4-Hour background scheduler active on all nodes.</div>
          </div>
          <div class="pt-1 flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400">
            <span>Log retention: 300 cycles</span>
            <button onclick="switchTab('diagnostics')" class="text-sky-600 dark:text-sky-400 font-bold hover:underline" data-i18n="open_diagnostics">AI Diagnostics →</button>
          </div>
        </div>

      </div>

    </section>

    <!-- ============================================================== -->
    <!-- SECTION 2: ZERO-LOSS SMART SCAN                               -->
    <!-- ============================================================== -->
    <section id="sec_smart_scan" class="section-view space-y-4">
      
      <!-- Smart Scan Controls Bar -->
      <div class="surface-card rounded-2xl p-4 sm:p-5 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="flex items-center gap-2">
            <h3 class="text-sm font-extrabold text-slate-900 dark:text-white" data-i18n="smart_scan_title">Zero-Loss Smart Scanner</h3>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-400" data-i18n="scan_only_default">Scan-Only Mode (Default)</span>
          </div>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5" data-i18n="smart_scan_sub">Accurate byte calculations with zero destructive operations until approved</p>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <button onclick="setCategoryPreset('all')" class="px-3 py-1.5 rounded-xl text-xs font-bold subtle-pill" data-i18n="select_all">Select All</button>
          <button onclick="setCategoryPreset('recommended')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-sky-600 text-white shadow-sm" data-i18n="recommended">Recommended</button>
          <button onclick="setCategoryPreset('none')" class="px-3 py-1.5 rounded-xl text-xs font-medium text-slate-500 hover:text-slate-800 dark:hover:text-white" data-i18n="clear_selection">Clear</button>
        </div>
      </div>

      <!-- 8 Cleanable Category Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        
        <!-- Category 1: User Temp -->
        <div class="surface-card rounded-2xl p-4 space-y-2 cursor-pointer transition-all hover:border-sky-300 dark:hover:border-sky-700" onclick="toggleCategoryCheckbox('chk_user_temp')">
          <div class="flex items-start justify-between">
            <div class="w-8 h-8 rounded-xl bg-sky-100 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300 flex items-center justify-center text-sm font-bold">📂</div>
            <input type="checkbox" id="chk_user_temp" checked class="w-4 h-4 rounded text-sky-600 focus:ring-sky-500" onclick="event.stopPropagation(); recalculateSelection();">
          </div>
          <h4 class="text-xs font-bold text-slate-900 dark:text-white" data-i18n="cat_user_temp">User Temp Files</h4>
          <p class="text-[11px] text-slate-500 dark:text-slate-400" data-i18n="cat_user_temp_desc">Disposable user application cache in %TEMP%</p>
          <div class="flex items-center justify-between text-xs font-mono pt-1">
            <span class="text-slate-500">729 items</span>
            <strong class="text-sky-600 dark:text-sky-400">28.7 MB</strong>
          </div>
        </div>

        <!-- Category 2: Windows Temp -->
        <div class="surface-card rounded-2xl p-4 space-y-2 cursor-pointer transition-all hover:border-sky-300 dark:hover:border-sky-700" onclick="toggleCategoryCheckbox('chk_win_temp')">
          <div class="flex items-start justify-between">
            <div class="w-8 h-8 rounded-xl bg-blue-100 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 flex items-center justify-center text-sm font-bold">🪟</div>
            <input type="checkbox" id="chk_win_temp" checked class="w-4 h-4 rounded text-sky-600 focus:ring-sky-500" onclick="event.stopPropagation(); recalculateSelection();">
          </div>
          <h4 class="text-xs font-bold text-slate-900 dark:text-white" data-i18n="cat_win_temp">Windows Temp</h4>
          <p class="text-[11px] text-slate-500 dark:text-slate-400" data-i18n="cat_win_temp_desc">Stale OS temp files in C:\Windows\Temp</p>
          <div class="flex items-center justify-between text-xs font-mono pt-1">
            <span class="text-slate-500">Admin mode</span>
            <strong class="text-sky-600 dark:text-sky-400">18.4 MB</strong>
          </div>
        </div>

        <!-- Category 3: Recycle Bin -->
        <div class="surface-card rounded-2xl p-4 space-y-2 cursor-pointer transition-all hover:border-sky-300 dark:hover:border-sky-700" onclick="toggleCategoryCheckbox('chk_recycle_bin')">
          <div class="flex items-start justify-between">
            <div class="w-8 h-8 rounded-xl bg-amber-100 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 flex items-center justify-center text-sm font-bold">🗑️</div>
            <input type="checkbox" id="chk_recycle_bin" checked class="w-4 h-4 rounded text-sky-600 focus:ring-sky-500" onclick="event.stopPropagation(); recalculateSelection();">
          </div>
          <h4 class="text-xs font-bold text-slate-900 dark:text-white" data-i18n="cat_recycle_bin">Recycle Bin</h4>
          <p class="text-[11px] text-slate-500 dark:text-slate-400" data-i18n="cat_recycle_bin_desc">Empties discarded files across local drives</p>
          <div class="flex items-center justify-between text-xs font-mono pt-1">
            <span class="text-slate-500">Optional</span>
            <strong class="text-sky-600 dark:text-sky-400">140.0 MB</strong>
          </div>
        </div>

        <!-- Category 4: Thumbnail & Icon Cache -->
        <div class="surface-card rounded-2xl p-4 space-y-2 cursor-pointer transition-all hover:border-sky-300 dark:hover:border-sky-700" onclick="toggleCategoryCheckbox('chk_thumb_cache')">
          <div class="flex items-start justify-between">
            <div class="w-8 h-8 rounded-xl bg-teal-100 dark:bg-teal-950/60 text-teal-700 dark:text-teal-300 flex items-center justify-center text-sm font-bold">🖼️</div>
            <input type="checkbox" id="chk_thumb_cache" checked class="w-4 h-4 rounded text-sky-600 focus:ring-sky-500" onclick="event.stopPropagation(); recalculateSelection();">
          </div>
          <h4 class="text-xs font-bold text-slate-900 dark:text-white" data-i18n="cat_thumb_cache">Thumbnail & Icons</h4>
          <p class="text-[11px] text-slate-500 dark:text-slate-400" data-i18n="cat_thumb_cache_desc">Rebuilds bloated explorer icon databases</p>
          <div class="flex items-center justify-between text-xs font-mono pt-1">
            <span class="text-slate-500">Explorer</span>
            <strong class="text-sky-600 dark:text-sky-400">62.5 MB</strong>
          </div>
        </div>

        <!-- Category 5: Prefetch & RAM Trim (Advanced, separately approved) -->
        <div class="surface-card rounded-2xl p-4 space-y-2 cursor-pointer transition-all hover:border-sky-300 dark:hover:border-sky-700 border-amber-300/80 dark:border-amber-700/60" onclick="toggleCategoryCheckbox('chk_prefetch_ram')">
          <div class="flex items-start justify-between">
            <div class="w-8 h-8 rounded-xl bg-rose-100 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 flex items-center justify-center text-sm font-bold">⚡</div>
            <input type="checkbox" id="chk_prefetch_ram" checked class="w-4 h-4 rounded text-sky-600 focus:ring-sky-500" onclick="event.stopPropagation(); recalculateSelection();">
          </div>
          <div class="flex items-center gap-1.5">
            <h4 class="text-xs font-bold text-slate-900 dark:text-white" data-i18n="cat_prefetch_ram">Prefetch & RAM Trim</h4>
            <span class="text-[9px] font-mono px-1 rounded bg-amber-100 text-amber-800">Advanced</span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400" data-i18n="cat_prefetch_desc">Trims bloated process working sets safely</p>
          <div class="flex items-center justify-between text-xs font-mono pt-1">
            <span class="text-slate-500">124 procs</span>
            <strong class="text-rose-600 dark:text-rose-400">512 MB</strong>
          </div>
        </div>

        <!-- Category 6: Windows Error & WER -->
        <div class="surface-card rounded-2xl p-4 space-y-2 cursor-pointer transition-all hover:border-sky-300 dark:hover:border-sky-700" onclick="toggleCategoryCheckbox('chk_win_error')">
          <div class="flex items-start justify-between">
            <div class="w-8 h-8 rounded-xl bg-purple-100 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300 flex items-center justify-center text-sm font-bold">⚠️</div>
            <input type="checkbox" id="chk_win_error" checked class="w-4 h-4 rounded text-sky-600 focus:ring-sky-500" onclick="event.stopPropagation(); recalculateSelection();">
          </div>
          <h4 class="text-xs font-bold text-slate-900 dark:text-white" data-i18n="cat_win_error">Windows Crash Dumps</h4>
          <p class="text-[11px] text-slate-500 dark:text-slate-400" data-i18n="cat_win_error_desc">Cleans stale WER crash logs older than 7d</p>
          <div class="flex items-center justify-between text-xs font-mono pt-1">
            <span class="text-slate-500">70 dumps</span>
            <strong class="text-purple-600 dark:text-purple-400">92.0 MB</strong>
          </div>
        </div>

        <!-- Category 7: Windows cleanmgr.exe Safe VolumeCaches -->
        <div class="surface-card rounded-2xl p-4 space-y-2 cursor-pointer transition-all hover:border-sky-300 dark:hover:border-sky-700" onclick="toggleCategoryCheckbox('chk_cleanmgr_safe')">
          <div class="flex items-start justify-between">
            <div class="w-8 h-8 rounded-xl bg-indigo-100 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 flex items-center justify-center text-sm font-bold">🧹</div>
            <input type="checkbox" id="chk_cleanmgr_safe" checked class="w-4 h-4 rounded text-sky-600 focus:ring-sky-500" onclick="event.stopPropagation(); recalculateSelection();">
          </div>
          <h4 class="text-xs font-bold text-slate-900 dark:text-white" data-i18n="cat_cleanmgr_safe">Windows cleanmgr.exe</h4>
          <p class="text-[11px] text-slate-500 dark:text-slate-400" data-i18n="cat_cleanmgr_desc">Native safe VolumeCaches sweep</p>
          <div class="flex items-center justify-between text-xs font-mono pt-1">
            <span class="text-slate-500">StateFlags</span>
            <strong class="text-indigo-600 dark:text-indigo-400">850 MB</strong>
          </div>
        </div>

        <!-- Category 8: Browser Shader Cache -->
        <div class="surface-card rounded-2xl p-4 space-y-2 cursor-pointer transition-all hover:border-sky-300 dark:hover:border-sky-700" onclick="toggleCategoryCheckbox('chk_shader_cache')">
          <div class="flex items-start justify-between">
            <div class="w-8 h-8 rounded-xl bg-cyan-100 dark:bg-cyan-950/60 text-cyan-700 dark:text-cyan-300 flex items-center justify-center text-sm font-bold">🎮</div>
            <input type="checkbox" id="chk_shader_cache" checked class="w-4 h-4 rounded text-sky-600 focus:ring-sky-500" onclick="event.stopPropagation(); recalculateSelection();">
          </div>
          <h4 class="text-xs font-bold text-slate-900 dark:text-white" data-i18n="cat_shader_cache">DirectX / Browser Shaders</h4>
          <p class="text-[11px] text-slate-500 dark:text-slate-400" data-i18n="cat_shader_desc">GPU and DirectX stale shader caches</p>
          <div class="flex items-center justify-between text-xs font-mono pt-1">
            <span class="text-slate-500">GPU cache</span>
            <strong class="text-cyan-600 dark:text-cyan-400">145 MB</strong>
          </div>
        </div>

      </div>

      <!-- Strict Protection & Exclusions Banner -->
      <div class="p-3.5 surface-card rounded-2xl border-emerald-200 dark:border-emerald-900/50 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
        <div class="flex items-center gap-2">
          <span class="text-lg">🔒</span>
          <div>
            <strong class="text-slate-900 dark:text-white" data-i18n="strict_exclusions_title">Protected Directories Policy:</strong>
            <span class="text-slate-600 dark:text-slate-300" data-i18n="strict_exclusions_desc"> Downloads, Documents, Desktop, and user document trees are never touched.</span>
          </div>
        </div>
        <div class="flex items-center gap-2 text-xs font-mono">
          <span>Age threshold:</span>
          <select id="selAgeLimit" class="bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-lg border border-slate-300 dark:border-slate-700">
            <option value="24" selected>24 hours (Default)</option>
            <option value="4">4 hours (Aggressive)</option>
            <option value="1">1 hour (Emergency)</option>
          </select>
        </div>
      </div>

    </section>

    <!-- ============================================================== -->
    <!-- SECTION 3: DETERMINISTIC AI DIAGNOSTICS                       -->
    <!-- ============================================================== -->
    <section id="sec_diagnostics" class="section-view space-y-4">
      
      <!-- Diagnostics Header & Alert Bar -->
      <div class="surface-card rounded-2xl p-4 sm:p-5 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 class="text-sm font-extrabold text-slate-900 dark:text-white" data-i18n="diagnostics_title">Deterministic Hardware Diagnostics</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400" data-i18n="diagnostics_sub">Win32 API live metrics, micro-probe disk latency, and evidence-based root causes</p>
        </div>
        <button onclick="refreshDiagnostics()" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-sky-600 text-white hover:bg-sky-700 transition-all shadow-sm">
          🔄 Run Live Telemetry Audit
        </button>
      </div>

      <!-- Live Win32 Telemetry Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        
        <!-- Metric 1: CPU Load -->
        <div class="surface-card rounded-2xl p-4 space-y-1.5">
          <span class="text-xs font-bold text-slate-500 dark:text-slate-400" data-i18n="metric_cpu">Win32 CPU Utilization</span>
          <div class="text-2xl font-black text-slate-900 dark:text-white font-mono" id="diagCpuText">32.5%</div>
          <div class="text-[11px] text-emerald-600 font-semibold" id="diagCpuStatus">🟢 Normal Operating Headroom</div>
        </div>

        <!-- Metric 2: RAM Saturation -->
        <div class="surface-card rounded-2xl p-4 space-y-1.5">
          <span class="text-xs font-bold text-slate-500 dark:text-slate-400" data-i18n="metric_ram">Physical RAM Saturation</span>
          <div class="text-2xl font-black text-slate-900 dark:text-white font-mono" id="diagRamText">78% (3.4 GB Free)</div>
          <div class="text-[11px] text-amber-600 font-semibold" id="diagRamStatus">⚠️ Elevated Working-Set Load</div>
        </div>

        <!-- Metric 3: Disk I/O Latency -->
        <div class="surface-card rounded-2xl p-4 space-y-1.5">
          <span class="text-xs font-bold text-slate-500 dark:text-slate-400" data-i18n="metric_latency">Disk I/O Micro-Probe Latency</span>
          <div class="text-2xl font-black text-slate-900 dark:text-white font-mono" id="diagLatencyText">2.15 ms</div>
          <div class="text-[11px] text-emerald-600 font-semibold">🟢 Ultra-Fast NVMe SSD Response</div>
        </div>

        <!-- Metric 4: Crash Reports -->
        <div class="surface-card rounded-2xl p-4 space-y-1.5">
          <span class="text-xs font-bold text-slate-500 dark:text-slate-400" data-i18n="metric_wer">WER Application Crash Manifests</span>
          <div class="text-2xl font-black text-slate-900 dark:text-white font-mono" id="diagCrashText">70 Logs</div>
          <div class="text-[11px] text-slate-500 font-semibold">Verified in WER ReportArchive</div>
        </div>

      </div>

      <!-- Top Processes Table & AI Root Cause Explanations -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        
        <!-- High-Resource Processes Table -->
        <div class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">
          <h4 class="text-xs font-extrabold uppercase tracking-wider text-slate-900 dark:text-white" data-i18n="high_resource_procs">High-Resource Win32 Processes</h4>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-mono">
              <thead class="border-b border-sky-100 dark:border-white/5 text-slate-500">
                <tr>
                  <th class="pb-2">Process Name</th>
                  <th class="pb-2">PID</th>
                  <th class="pb-2 text-right">Physical Memory</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-white/5" id="diagProcsTableBody">
                <tr><td class="py-2 font-bold text-slate-800 dark:text-slate-200">Memory Compression</td><td>2152</td><td class="text-right text-sky-600 font-bold">1,580 MB</td></tr>
                <tr><td class="py-2 font-bold text-slate-800 dark:text-slate-200">language_server.exe</td><td>11964</td><td class="text-right text-sky-600 font-bold">794 MB</td></tr>
                <tr><td class="py-2 font-bold text-slate-800 dark:text-slate-200">chrome.exe</td><td>5856</td><td class="text-right text-sky-600 font-bold">492 MB</td></tr>
                <tr><td class="py-2 font-bold text-slate-800 dark:text-slate-200">chrome.exe</td><td>6120</td><td class="text-right text-sky-600 font-bold">484 MB</td></tr>
                <tr><td class="py-2 font-bold text-slate-800 dark:text-slate-200">chrome.exe</td><td>4796</td><td class="text-right text-sky-600 font-bold">405 MB</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Evidence-Based Root Cause Explanations -->
        <div class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between border-b border-sky-100 dark:border-white/5 pb-2">
              <h4 class="text-xs font-extrabold uppercase tracking-wider text-slate-900 dark:text-white" data-i18n="root_cause_title">Evidence-Based Diagnostic Summary</h4>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-sky-100 text-sky-700 dark:bg-sky-950/60 dark:text-sky-300">DETERMINISTIC</span>
            </div>
            <div class="mt-3 space-y-2 text-xs leading-relaxed text-slate-700 dark:text-slate-300">
              <p>• <strong>Primary Constraint:</strong> Memory saturation (78%) is driven by active browser renderers and compiler language servers. Working-set pages are eligible for safe Win32 compaction without terminating applications.</p>
              <p>• <strong>Storage Headroom:</strong> C: drive has 10.3 GB free (91.4% full). Zero file system corruption detected; disk latency benchmark is optimal at 2.15 ms.</p>
              <p>• <strong>Safety Recommendation:</strong> <span class="text-sky-600 font-bold">[LOW RISK]</span> Execute Safe Temp Cleanup and process working-set release.</p>
            </div>
          </div>
          <div class="pt-2 flex items-center gap-2">
            <button onclick="triggerAntiHangRescue()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-rose-50 text-rose-700 border border-rose-300 hover:bg-rose-100 transition-all flex items-center gap-1.5 shadow-sm active:scale-95">
              <span>🚨</span><span>Flush Working Set Now</span>
            </button>
            <button onclick="triggerCleanSelected()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-sky-600 text-white hover:bg-sky-700 transition-all shadow-sm active:scale-95">
              <span>⚡</span><span>Execute Safe Clean</span>
            </button>
          </div>
        </div>

      </div>

      <!-- Quick AI Diagnostic Scenarios (6 Core Prompts) -->
      <div class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">
        <h4 class="text-xs font-extrabold uppercase tracking-wider text-slate-900 dark:text-white" data-i18n="copilot_quick_title">AI Technician Copilot — 6 Core Diagnostic Inquiries</h4>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
          <button onclick="openAIChatWithPrompt('Why is my computer slow?')" class="p-3 rounded-xl border border-sky-100 dark:border-white/5 bg-sky-50/50 hover:bg-sky-100/60 dark:bg-slate-900/50 dark:hover:bg-slate-800/60 text-left transition-all active:scale-95">
            <div class="text-xs font-bold text-sky-800 dark:text-sky-300">1. Why is my computer slow?</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">என் கணினி ஏன் மெதுவாக உள்ளது?</div>
          </button>
          <button onclick="openAIChatWithPrompt('Which NUNES computer needs attention?')" class="p-3 rounded-xl border border-sky-100 dark:border-white/5 bg-sky-50/50 hover:bg-sky-100/60 dark:bg-slate-900/50 dark:hover:bg-slate-800/60 text-left transition-all active:scale-95">
            <div class="text-xs font-bold text-sky-800 dark:text-sky-300">2. Which NUNES PC needs attention?</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">எந்த கணினிக்கு கவனம் தேவை?</div>
          </button>
          <button onclick="openAIChatWithPrompt('How much storage can be safely recovered?')" class="p-3 rounded-xl border border-sky-100 dark:border-white/5 bg-sky-50/50 hover:bg-sky-100/60 dark:bg-slate-900/50 dark:hover:bg-slate-800/60 text-left transition-all active:scale-95">
            <div class="text-xs font-bold text-sky-800 dark:text-sky-300">3. How much storage can be recovered?</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">எவ்வளவு சேமிப்பகம் மீட்க முடியும்?</div>
          </button>
          <button onclick="openAIChatWithPrompt('Show the last 30 days of disk usage.')" class="p-3 rounded-xl border border-sky-100 dark:border-white/5 bg-sky-50/50 hover:bg-sky-100/60 dark:bg-slate-900/50 dark:hover:bg-slate-800/60 text-left transition-all active:scale-95">
            <div class="text-xs font-bold text-sky-800 dark:text-sky-300">4. Show last 30 days disk usage</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">கடந்த 30 நாட்களின் வட்டு பயன்பாடு</div>
          </button>
          <button onclick="openAIChatWithPrompt('Why is the Accounts PC freezing?')" class="p-3 rounded-xl border border-sky-100 dark:border-white/5 bg-sky-50/50 hover:bg-sky-100/60 dark:bg-slate-900/50 dark:hover:bg-slate-800/60 text-left transition-all active:scale-95">
            <div class="text-xs font-bold text-sky-800 dark:text-sky-300">5. Why is Accounts PC freezing?</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">கணக்கு பிரிவு கணினி ஏன் உறைகிறது?</div>
          </button>
          <button onclick="openAIChatWithPrompt('Generate a maintenance report.')" class="p-3 rounded-xl border border-sky-100 dark:border-white/5 bg-sky-50/50 hover:bg-sky-100/60 dark:bg-slate-900/50 dark:hover:bg-slate-800/60 text-left transition-all active:scale-95">
            <div class="text-xs font-bold text-sky-800 dark:text-sky-300">6. Generate a maintenance report</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">பராமரிப்பு அறிக்கையை உருவாக்கு</div>
          </button>
        </div>
      </div>

    </section>
'''
print("Loaded Part 3")
