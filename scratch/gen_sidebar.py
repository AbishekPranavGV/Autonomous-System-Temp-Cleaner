# -*- coding: utf-8 -*-
import sys
import os

def generate_sidebar_html():
    return """
    <!-- 🌟 COLLAPSIBLE SIDEBAR (Enterprise vNext) -->
    <aside id="appSidebar" class="hidden lg:flex flex-col w-64 bg-white/95 dark:bg-slate-900/95 border-r border-sky-100 dark:border-white/10 shrink-0 transition-all duration-300 z-30 select-none">
      <!-- Sidebar Brand Header -->
      <div class="h-16 flex items-center justify-between px-4 border-b border-sky-100 dark:border-white/10">
        <div class="flex items-center gap-2.5 overflow-hidden sidebar-text">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white font-black text-sm shadow-sm shadow-sky-500/30 shrink-0">
            N
          </div>
          <div class="leading-tight">
            <span class="font-extrabold text-sm tracking-tight text-slate-900 dark:text-white block">NUNES AI PC</span>
            <span class="text-[10px] font-mono text-sky-600 dark:text-sky-400 font-bold">v10.1 ENTERPRISE</span>
          </div>
        </div>
        <button onclick="toggleSidebarCollapse()" id="btnSidebarCollapse" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all" title="Collapse / Expand Sidebar">
          <span id="collapseIcon" class="text-xs">◀</span>
        </button>
      </div>

      <!-- Navigation Links -->
      <div class="flex-1 py-4 px-2 space-y-1 overflow-y-auto scrollbar-none font-semibold text-xs" role="tablist">
        <button onclick="switchTab('overview')" id="sideBtn_overview" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl bg-sky-50 text-sky-700 dark:bg-sky-950/60 dark:text-sky-300 font-bold transition-all sidebar-nav-btn active">
          <span class="text-base shrink-0">📊</span>
          <span class="sidebar-text truncate" data-i18n="nav_overview">1. Dashboard</span>
        </button>
        <button onclick="switchTab('smart_scan')" id="sideBtn_smart_scan" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5 transition-all sidebar-nav-btn">
          <span class="text-base shrink-0">🔍</span>
          <span class="sidebar-text truncate" data-i18n="nav_smart_scan">2. Smart Scan</span>
        </button>
        <button onclick="switchTab('diagnostics')" id="sideBtn_diagnostics" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5 transition-all sidebar-nav-btn">
          <span class="text-base shrink-0">🩺</span>
          <span class="sidebar-text truncate" data-i18n="nav_diagnostics">3. AI Diagnostics</span>
        </button>
        <button onclick="switchTab('cleanup')" id="sideBtn_cleanup" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5 transition-all sidebar-nav-btn">
          <span class="text-base shrink-0">⚡</span>
          <span class="sidebar-text truncate" data-i18n="nav_cleanup">4. Safe Cleanup</span>
        </button>
        <button onclick="switchTab('fleet')" id="sideBtn_fleet" class="w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5 transition-all sidebar-nav-btn">
          <div class="flex items-center gap-3 overflow-hidden">
            <span class="text-base shrink-0">🖥️</span>
            <span class="sidebar-text truncate" data-i18n="nav_fleet">5. Fleet Command</span>
          </div>
          <span class="sidebar-text px-1.5 py-0.5 rounded-full text-[10px] font-mono bg-sky-100 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300 font-bold">4</span>
        </button>
        <button onclick="switchTab('health')" id="sideBtn_health" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5 transition-all sidebar-nav-btn">
          <span class="text-base shrink-0">❤️</span>
          <span class="sidebar-text truncate" data-i18n="nav_health">6. System Health</span>
        </button>
        <button onclick="switchTab('reports')" id="sideBtn_reports" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5 transition-all sidebar-nav-btn">
          <span class="text-base shrink-0">📋</span>
          <span class="sidebar-text truncate" data-i18n="nav_reports">7. Reports & Audit</span>
        </button>
        <button onclick="switchTab('settings')" id="sideBtn_settings" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5 transition-all sidebar-nav-btn">
          <span class="text-base shrink-0">⚙️</span>
          <span class="sidebar-text truncate" data-i18n="nav_settings">8. Settings</span>
        </button>
      </div>

      <!-- Sidebar Bottom Fleet Status Card -->
      <div class="p-3 border-t border-sky-100 dark:border-white/10 sidebar-text">
        <div class="p-3 rounded-xl bg-sky-50/70 dark:bg-slate-800/60 border border-sky-100 dark:border-white/5 space-y-1.5">
          <div class="flex items-center justify-between text-[11px]">
            <span class="text-slate-500 dark:text-slate-400 font-bold">Fleet Health</span>
            <span class="font-mono font-black text-emerald-600 dark:text-emerald-400">99.8%</span>
          </div>
          <div class="w-full bg-slate-200 dark:bg-slate-700 h-1.5 rounded-full overflow-hidden">
            <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 99.8%"></div>
          </div>
          <div class="flex items-center justify-between text-[10px] text-slate-400 font-mono pt-0.5">
            <span>30D RETENTION</span>
            <span class="text-sky-600 dark:text-sky-400 font-bold">ACTIVE</span>
          </div>
        </div>
      </div>
    </aside>
    """

print("Sidebar HTML generator ready!")
