# -*- coding: utf-8 -*-
import sys
import os

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Helper HTML components
HEADER_SEARCH_AND_NOTIFICATIONS = """
        <!-- 🔍 Global Fleet & Command Search -->
        <div class="relative flex-1 max-w-xs sm:max-w-sm hidden md:block">
          <input type="text" id="globalFleetSearch" oninput="handleGlobalFleetSearch(this.value)" placeholder="Search workstations, IP, status, tools..." class="w-full h-8 pl-8 pr-3 text-xs rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-white/10 text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-sky-500 transition-all font-mono">
          <span class="absolute left-2.5 top-2 text-xs text-slate-400">🔍</span>
        </div>

        <!-- 🔔 Unified Notification & Warning Center -->
        <div class="relative" id="notificationCenterContainer">
          <button onclick="toggleNotificationCenter(event)" id="btnNotificationCenter" class="relative p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all flex items-center justify-center active:scale-95" title="Notifications & System Warnings">
            <span class="text-sm">🔔</span>
            <span id="notificationBadgeCount" class="absolute -top-0.5 -right-0.5 w-4 h-4 rounded-full bg-rose-500 text-white font-mono text-[9px] font-black flex items-center justify-center animate-pulse">2</span>
          </button>

          <!-- Notification Dropdown Flyout -->
          <div id="notificationDropdownPanel" class="hidden absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl bg-white/95 dark:bg-[#111d38]/95 backdrop-blur-xl border border-sky-200 dark:border-white/10 shadow-2xl z-50 p-3 space-y-2.5 transition-all duration-200">
            <div class="flex items-center justify-between pb-2 border-b border-sky-100 dark:border-white/5 px-1">
              <div class="flex items-center gap-1.5">
                <span class="text-sm">🔔</span>
                <span class="text-xs font-extrabold text-slate-900 dark:text-white uppercase tracking-wider">System Warnings & Alerts</span>
              </div>
              <button onclick="clearNotifications()" class="text-[10px] text-sky-600 dark:text-sky-400 hover:underline font-bold">Mark Read</button>
            </div>

            <div class="space-y-2 max-h-72 overflow-y-auto scrollbar-none text-xs" id="notificationItemsList">
              <!-- Item 1: Storage Alert -->
              <div class="p-2.5 rounded-xl bg-amber-50/70 dark:bg-amber-950/30 border border-amber-200/60 dark:border-amber-800/40 flex items-start gap-2.5">
                <span class="text-amber-600 text-sm mt-0.5">⚠️</span>
                <div class="flex-1 space-y-0.5">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-slate-900 dark:text-white text-[11px]">DESKTOP-M378M07 Storage Alert</span>
                    <span class="text-[9px] font-mono text-slate-400">10:04 UTC</span>
                  </div>
                  <p class="text-[11px] text-slate-600 dark:text-slate-300">Free storage at 10.3 GB (approaching 10.0 GB threshold). 1.49 GB reclaimable.</p>
                  <button onclick="openCleanupWorkflow('DESKTOP-M378M07'); toggleNotificationCenter();" class="mt-1 text-[10px] font-bold text-amber-700 dark:text-amber-400 hover:underline">Launch Safe Clean →</button>
                </div>
              </div>

              <!-- Item 2: Memory Warning -->
              <div class="p-2.5 rounded-xl bg-rose-50/70 dark:bg-rose-950/30 border border-rose-200/60 dark:border-rose-800/40 flex items-start gap-2.5">
                <span class="text-rose-600 text-sm mt-0.5">🚨</span>
                <div class="flex-1 space-y-0.5">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-slate-900 dark:text-white text-[11px]">Elevated RAM Pressure</span>
                    <span class="text-[9px] font-mono text-slate-400">10:00 UTC</span>
                  </div>
                  <p class="text-[11px] text-slate-600 dark:text-slate-300">Host RAM working set at 78%. Hang resolver ready for process trim.</p>
                  <button onclick="triggerAntiHangRescue(); toggleNotificationCenter();" class="mt-1 text-[10px] font-bold text-rose-700 dark:text-rose-400 hover:underline">Execute Rescue Now →</button>
                </div>
              </div>

              <!-- Item 3: Retention Status -->
              <div class="p-2.5 rounded-xl bg-sky-50/70 dark:bg-sky-950/30 border border-sky-200/60 dark:border-sky-800/40 flex items-start gap-2.5">
                <span class="text-sky-600 text-sm mt-0.5">🛡️</span>
                <div class="flex-1 space-y-0.5">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-slate-900 dark:text-white text-[11px]">30-Day Unified Retention</span>
                    <span class="text-[9px] font-mono text-slate-400">04:00 UTC</span>
                  </div>
                  <p class="text-[11px] text-slate-600 dark:text-slate-300">48 snapshot archives verified. Auto-pruning strictly preserves 30 days.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
"""

CLEANUP_WORKFLOW_MODAL_HTML = """
  <!-- 🌟 ENTERPRISE 4-STEP CLEANUP WORKFLOW MODAL (Scan -> Review -> Approve -> Verify) -->
  <div id="cleanupWorkflowModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/60 backdrop-blur-md transition-all duration-300">
    <div class="surface-card w-full max-w-2xl rounded-2xl shadow-2xl border border-sky-200 dark:border-white/10 overflow-hidden flex flex-col max-h-[90vh]">
      
      <!-- Modal Header -->
      <div class="p-4 sm:p-5 border-b border-sky-100 dark:border-white/10 flex items-center justify-between bg-sky-50/50 dark:bg-slate-900/50">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-sky-600 text-white flex items-center justify-center font-black text-base shadow-sm">
            ⚡
          </div>
          <div>
            <h3 class="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
              <span>Zero-Loss Safe Cleanup Workflow</span>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-sky-100 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300">STEP <span id="cwStepNum">1</span> OF 4</span>
            </h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Strictly enforced safety allowlists & 30-day snapshot verification</p>
          </div>
        </div>
        <button onclick="closeCleanupWorkflow()" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">✕</button>
      </div>

      <!-- Step Progress Bar -->
      <div class="grid grid-cols-4 border-b border-slate-100 dark:border-white/5 text-[11px] font-bold text-center">
        <div id="cwStepTab1" class="py-2.5 bg-sky-600 text-white transition-all">1. Scan</div>
        <div id="cwStepTab2" class="py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 transition-all">2. Review</div>
        <div id="cwStepTab3" class="py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 transition-all">3. Approve</div>
        <div id="cwStepTab4" class="py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 transition-all">4. Verify</div>
      </div>

      <!-- Modal Body (Dynamic Steps) -->
      <div class="p-4 sm:p-5 flex-1 overflow-y-auto space-y-4 text-xs">
        
        <!-- Step 1: Scan Summary -->
        <div id="cwStepContent1" class="space-y-3">
          <div class="p-3.5 rounded-xl bg-sky-50 dark:bg-sky-950/30 border border-sky-100 dark:border-sky-900/50 flex items-center justify-between">
            <div>
              <span class="text-slate-400 block text-[10px] uppercase font-bold">Reclaimable Space</span>
              <strong class="text-2xl font-black text-sky-700 dark:text-sky-300">1.49 GB</strong>
            </div>
            <div class="text-right">
              <span class="text-slate-400 block text-[10px] uppercase font-bold">Candidate Files</span>
              <strong class="text-base font-bold text-slate-800 dark:text-slate-200">920 Files in 8 Categories</strong>
            </div>
          </div>
          <p class="text-slate-600 dark:text-slate-300 text-xs">
            Scan-only mode verified zero process interruptions. Candidate files have been analyzed against active Windows file locks.
          </p>
        </div>

        <!-- Step 2: Manifest Review -->
        <div id="cwStepContent2" class="hidden space-y-3">
          <div class="space-y-1.5 font-mono text-[11px]">
            <div class="flex justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-900/60">
              <span>Windows cleanmgr.exe (Update/Delivery Cache)</span>
              <strong class="text-sky-600">850.0 MB</strong>
            </div>
            <div class="flex justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-900/60">
              <span>Prefetch & RAM Working-Set Trim</span>
              <strong class="text-amber-600">512.0 MB</strong>
            </div>
            <div class="flex justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-900/60">
              <span>Browser GPU/DirectX Shader Cache</span>
              <strong class="text-teal-600">145.0 MB</strong>
            </div>
            <div class="flex justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-900/60">
              <span>Windows Error Reporting (WER) Dumps</span>
              <strong class="text-indigo-600">92.0 MB</strong>
            </div>
            <div class="flex justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-900/60">
              <span>User Temporary Files (%TEMP%)</span>
              <strong class="text-sky-600">28.7 MB</strong>
            </div>
          </div>

          <div class="p-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-900/50 flex items-center gap-2 text-emerald-800 dark:text-emerald-300 font-semibold text-[11px]">
            <span>🛡️</span>
            <span>Zero-Loss Guarantee: Downloads, Documents, Desktop, and Program Files are strictly blocked from deletion.</span>
          </div>
        </div>

        <!-- Step 3: Admin Approval -->
        <div id="cwStepContent3" class="hidden space-y-3">
          <div class="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/50 space-y-2">
            <span class="font-bold text-amber-900 dark:text-amber-300 flex items-center gap-1.5">
              <span>⚠️</span> Administrator Policy Authorization Required
            </span>
            <p class="text-slate-600 dark:text-slate-300 text-xs">
              A rollback snapshot will be created in the 30-Day Unified Retention archive before any file removal begins.
            </p>
          </div>

          <label class="flex items-start gap-2.5 p-3 rounded-xl border border-sky-100 dark:border-white/5 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-900/40 transition-all">
            <input type="checkbox" id="cwAdminConfirmCheck" class="w-4 h-4 rounded text-sky-600 focus:ring-sky-500 mt-0.5">
            <span class="text-xs text-slate-700 dark:text-slate-300 font-medium">
              I authorize the safe purge of verified candidate temporary cache files and confirm that pre-action snapshot retention is verified.
            </span>
          </label>
        </div>

        <!-- Step 4: Verification -->
        <div id="cwStepContent4" class="hidden space-y-3 text-center py-4">
          <div class="w-12 h-12 rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 mx-auto flex items-center justify-center text-xl font-black" id="cwVerifyIcon">
            ✓
          </div>
          <h4 class="font-bold text-sm text-slate-900 dark:text-white" id="cwVerifyTitle">Action Executed & Verified</h4>
          <p class="text-xs text-slate-500 dark:text-slate-400" id="cwVerifyDesc">
            880.29 MB safely recovered. Disk latency verified at 2.15 ms. Pre-clean snapshot cataloged in 30-day retention store.
          </p>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-4 sm:p-5 border-t border-sky-100 dark:border-white/10 flex items-center justify-between bg-slate-50 dark:bg-slate-900/50">
        <button onclick="prevCleanupWorkflowStep()" id="btnCwPrev" class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-all hidden">
          ← Back
        </button>
        <div class="flex items-center gap-2 ml-auto">
          <button onclick="closeCleanupWorkflow()" class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-500 hover:text-slate-700 dark:hover:text-slate-200 transition-all">
            Cancel
          </button>
          <button onclick="nextCleanupWorkflowStep()" id="btnCwNext" class="px-5 py-2 rounded-xl text-xs font-bold bg-sky-600 hover:bg-sky-700 text-white shadow-sm transition-all active:scale-95">
            Proceed to Review →
          </button>
        </div>
      </div>

    </div>
  </div>
"""

NODE_DETAIL_DRAWER_HTML = """
  <!-- 🌟 WORKSTATION DEEP DIAGNOSTIC INSPECTOR DRAWER -->
  <div id="nodeDetailDrawer" class="hidden fixed inset-0 z-50 flex justify-end bg-slate-950/50 backdrop-blur-sm transition-all duration-300">
    <div class="w-full max-w-md bg-white dark:bg-slate-900 h-full shadow-2xl border-l border-sky-100 dark:border-white/10 flex flex-col p-5 space-y-4 overflow-y-auto">
      
      <!-- Drawer Header -->
      <div class="flex items-center justify-between border-b border-sky-100 dark:border-white/10 pb-3">
        <div>
          <div class="flex items-center gap-2">
            <h3 class="font-mono font-bold text-base text-slate-900 dark:text-white" id="ndDrawerHostname">DESKTOP-M378M07</h3>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800" id="ndDrawerStatus">ONLINE</span>
          </div>
          <p class="text-xs text-sky-600 dark:text-sky-400 font-semibold mt-0.5" id="ndDrawerRole">Host PC (Direct Win32 Access)</p>
        </div>
        <button onclick="closeNodeDetailDrawer()" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">✕</button>
      </div>

      <!-- Telemetry Grid -->
      <div class="grid grid-cols-2 gap-2 text-xs font-mono">
        <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-sky-100 dark:border-white/5 space-y-1">
          <span class="text-slate-400 text-[10px] block">Free Storage</span>
          <strong class="text-slate-900 dark:text-white text-sm" id="ndDrawerFree">10.3 GB</strong>
        </div>
        <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-sky-100 dark:border-white/5 space-y-1">
          <span class="text-slate-400 text-[10px] block">RAM Load</span>
          <strong class="text-amber-600 text-sm" id="ndDrawerRam">78%</strong>
        </div>
        <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-sky-100 dark:border-white/5 space-y-1">
          <span class="text-slate-400 text-[10px] block">Disk Latency</span>
          <strong class="text-emerald-600 text-sm" id="ndDrawerLatency">2.15 ms</strong>
        </div>
        <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-sky-100 dark:border-white/5 space-y-1">
          <span class="text-slate-400 text-[10px] block">Network IP</span>
          <strong class="text-indigo-600 text-sm" id="ndDrawerIp">127.0.0.1</strong>
        </div>
      </div>

      <!-- Process Inspector -->
      <div class="space-y-2">
        <span class="text-xs font-extrabold uppercase tracking-wider text-slate-900 dark:text-white">Active High-Resource Processes</span>
        <div class="space-y-1 text-xs font-mono" id="ndDrawerProcesses">
          <div class="flex justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800/40"><span>chrome.exe</span><strong>482.4 MB</strong></div>
          <div class="flex justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800/40"><span>Code.exe</span><strong>388.9 MB</strong></div>
          <div class="flex justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800/40"><span>python.exe</span><strong>142.6 MB</strong></div>
        </div>
      </div>

      <!-- Rollback & Retention Box -->
      <div class="p-3 rounded-xl bg-sky-50/70 dark:bg-sky-950/40 border border-sky-100 dark:border-sky-900/60 space-y-1 text-xs">
        <span class="font-bold text-sky-800 dark:text-sky-300">30-Day Unified Retention</span>
        <p class="text-slate-600 dark:text-slate-300 text-[11px]">This node is protected under rolling 30-day snapshot policy. Rollback points ready.</p>
      </div>

      <!-- Remote Control Actions -->
      <div class="pt-2 border-t border-sky-100 dark:border-white/10 grid grid-cols-2 gap-2">
        <button onclick="triggerDirectRescueFromDrawer()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 transition-all">🚨 Rescue PC</button>
        <button onclick="triggerDirectCleanFromDrawer()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-sky-600 hover:bg-sky-700 text-white shadow-sm transition-all">⚡ Safe Clean</button>
      </div>

    </div>
  </div>
"""

print("Components ready for assembly.")
