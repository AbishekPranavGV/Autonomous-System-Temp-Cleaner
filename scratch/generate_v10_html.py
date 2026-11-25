# Python script to generate the complete production-grade index.html for NUNES AI PC Command Center v10.0
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

html_content = '''<!DOCTYPE html>
<html lang="en" class="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NUNES AI PC Command Center — Version 10.0 | Enterprise Windows Diagnostics & Fleet Sentry</title>
  <meta name="description" content="Production-grade Windows optimization, deterministic diagnostics, zero-loss cleanup, and secure fleet management for NUNES Instruments office computers.">

  <!-- Google Fonts: Plus Jakarta Sans & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            brand: {
              50: '#f0f7ff',
              100: '#e0f2fe',
              200: '#bae6fd',
              300: '#7dd3fc',
              400: '#38bdf8',
              500: '#0ea5e9',
              600: '#0284c7',
              700: '#0369a1',
              800: '#075985',
              900: '#0c4a6e',
            }
          }
        }
      }
    };
  </script>

  <style>
    /* Professional Light-Blue & Crisp White Theme */
    html.light body {
      background-color: #f0f7ff;
      background-image: 
        radial-gradient(circle at 10% 10%, rgba(2, 132, 199, 0.08) 0%, transparent 45%),
        radial-gradient(circle at 90% 90%, rgba(14, 165, 233, 0.06) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(224, 242, 254, 0.35) 0%, transparent 60%);
      color: #0f172a;
    }

    html.light .app-window, html.light .surface-card {
      background: #ffffff;
      border: 1px solid #e0f2fe;
      box-shadow: 0 10px 30px -10px rgba(2, 132, 199, 0.07), 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    html.light .primary-btn {
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: #ffffff;
    }

    html.light .subtle-pill {
      background: #f0f7ff;
      border: 1px solid #bae6fd;
      color: #0369a1;
    }

    /* Dark Theme */
    html.dark body {
      background-color: #0b1329;
      background-image: 
        radial-gradient(circle at 50% 20%, rgba(14, 165, 233, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(2, 132, 199, 0.05) 0%, transparent 50%);
      color: #f8fafc;
    }

    html.dark .app-window, html.dark .surface-card {
      background: #111d38;
      border: 1px solid rgba(56, 189, 248, 0.15);
      box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
    }

    html.dark .primary-btn {
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: #ffffff;
    }

    html.dark .subtle-pill {
      background: rgba(14, 165, 233, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: #38bdf8;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(100, 116, 139, 0.3); border-radius: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(100, 116, 139, 0.5); }

    /* Tab navigation buttons */
    .nav-tab-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.375rem;
      padding: 0.45rem 0.85rem;
      border-radius: 0.75rem;
      font-size: 0.75rem;
      font-weight: 700;
      white-space: nowrap;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      color: #64748b;
    }
    html.dark .nav-tab-btn { color: #94a3b8; }

    .nav-tab-btn:hover {
      color: #0284c7;
      background: rgba(2, 132, 199, 0.08);
    }
    html.dark .nav-tab-btn:hover {
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
    }

    .nav-tab-btn.active {
      color: #ffffff !important;
      background: #0284c7 !important;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    }

    .section-view {
      display: none;
      animation: fadeIn 0.25s ease-out forwards;
    }
    .section-view.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>

<body class="min-h-screen py-3 px-2 sm:px-4 text-slate-800 dark:text-slate-100 font-sans antialiased">

  <!-- Main Application Window Wrapper -->
  <div class="w-full max-w-[99%] 2xl:max-w-[1680px] mx-auto app-window rounded-2xl sm:rounded-3xl p-3 sm:p-4 md:p-5 space-y-3 sm:space-y-4 transition-all duration-300">

    <!-- Top Header Bar with Brand, Live Clock, Language Toggle, and Actions -->
    <header class="flex flex-col xl:flex-row items-start xl:items-center justify-between gap-3 pb-3 border-b border-sky-100 dark:border-sky-950/60">
      
      <!-- Brand Area: NUNES AI PC Command Center v10.0 -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-sky-600 via-blue-600 to-indigo-700 flex items-center justify-center shadow-md shadow-sky-500/25 text-white font-black text-lg select-none flex-shrink-0 animate-pulse">
          ⚡
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl sm:text-2xl font-black tracking-tight text-slate-900 dark:text-white" id="mainAppTitle">
              NUNES AI PC Command Center
            </h1>
            <span class="text-[10px] font-mono font-bold text-sky-700 dark:text-sky-300 bg-sky-100 dark:bg-sky-950/70 border border-sky-300 dark:border-sky-800 px-2 py-0.5 rounded-full" id="versionBadge">
              v10.0 Enterprise
            </span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium" id="subAppTitle">
            Autonomous Optimization, Deterministic Win32 Diagnostics & Fleet Sentry • NUNES Instruments
          </p>
        </div>

        <!-- Hidden ID Anchors to preserve existing backend/DOM references -->
        <span id="adminBadge" class="hidden"></span>
        <span id="scanStatusBadge" class="hidden"><span id="scanStatusText"></span></span>
        <span id="nextLoopClock" class="hidden"></span>
      </div>

      <!-- Header Operational Actions (Clock, Language, Theme, Scan, Clean, Rescue, Settings) -->
      <div class="flex flex-wrap items-center gap-2 w-full xl:w-auto justify-end">
        
        <!-- Live Real-Time Heartbeat Clock -->
        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-sky-50 dark:bg-sky-950/50 text-sky-700 dark:text-sky-300 border border-sky-200 dark:border-sky-800/80 text-xs font-mono font-bold shadow-sm">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span id="liveStatusClock">LIVE • Updated</span>
        </div>

        <!-- 🌐 Language Switcher (English / தமிழ்) -->
        <button onclick="toggleLanguage()" id="btnLangToggle" class="px-3 py-1.5 rounded-xl text-xs font-extrabold bg-white dark:bg-slate-800 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-slate-200 hover:border-sky-500 transition-all flex items-center gap-1.5 shadow-sm active:scale-95" title="Switch Language (English / தமிழ்)">
          <span class="text-sm">🌐</span>
          <span id="langToggleLabel">தமிழ்</span>
        </button>

        <!-- 🌙 Theme Toggle Button -->
        <button onclick="toggleTheme()" id="btnThemeToggle" class="w-8 h-8 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-white/10 text-slate-700 dark:text-slate-200 hover:border-sky-500 flex items-center justify-center text-xs shadow-sm active:scale-95 transition-all" title="Toggle Light/Dark Theme">
          <span id="themeToggleIcon">🌙</span>
        </button>

        <!-- 🔍 Scan Selected Button -->
        <button onclick="triggerScanSelected()" id="btnScanSelected" class="px-3.5 py-1.5 rounded-xl text-xs font-bold subtle-pill border-sky-300 hover:border-sky-400 dark:border-sky-600/50 text-sky-700 dark:text-sky-300 transition-all flex items-center gap-1.5 active:scale-95 shadow-sm" title="Scan selected categories">
          <span>🔍</span>
          <span data-i18n="btn_scan">Scan Selected</span>
        </button>

        <!-- ⚡ CLEAN SELECTED (Primary Action) -->
        <button onclick="triggerCleanSelected()" id="btnCleanSelected" class="px-4.5 py-1.5 rounded-xl text-xs font-black uppercase tracking-wider primary-btn transition-all flex items-center gap-2 active:scale-95 shadow-md shadow-sky-600/30" title="Safely clean junk files">
          <span>⚡</span>
          <span data-i18n="btn_clean">CLEAN SELECTED</span>
        </button>

        <!-- 🚨 Anti-Hang Rescue Button -->
        <button onclick="triggerAntiHangRescue()" id="btnAntiHang" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold uppercase bg-rose-50 hover:bg-rose-100 dark:bg-rose-950/40 dark:hover:bg-rose-900/50 text-rose-700 dark:text-rose-400 border border-rose-300 dark:border-rose-700/50 transition-all flex items-center gap-1.5 active:scale-95 shadow-sm" title="Emergency RAM Trim & Frozen Process Resolver">
          <span>🚨</span>
          <span data-i18n="btn_rescue">RESCUE PC</span>
        </button>

        <!-- ⚙️ Top Settings Flyout / Tab Shortcut -->
        <div class="relative" id="settingsContainer">
          <button onclick="toggleSettingsMenu(event)" id="btnTopSettings" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white dark:bg-white dark:hover:bg-slate-100 dark:text-slate-900 shadow-md transition-all flex items-center gap-1.5 active:scale-95" title="Settings & Utilities">
            <span class="text-sm">⚙️</span>
            <span data-i18n="nav_settings">Settings</span>
            <span class="text-[9px] opacity-70 transition-transform duration-200" id="settingsArrow">▼</span>
          </button>

          <!-- Settings Dropdown Flyout Panel -->
          <div id="settingsDropdownMenu" class="hidden absolute right-0 mt-2 w-72 sm:w-80 rounded-2xl bg-white/95 dark:bg-[#111d38]/95 backdrop-blur-xl border border-sky-200 dark:border-white/10 shadow-2xl z-50 p-3 space-y-2 transition-all duration-200">
            <div class="flex items-center justify-between pb-2 border-b border-sky-100 dark:border-white/5 px-1">
              <div class="flex items-center gap-1.5">
                <span class="text-sm">⚙️</span>
                <span class="text-xs font-extrabold text-slate-900 dark:text-white uppercase tracking-wider">Quick Utilities</span>
              </div>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-sky-100 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300 font-bold">v10.0</span>
            </div>

            <div class="space-y-1 text-xs">
              <button onclick="switchTab('settings'); toggleSettingsMenu();" class="w-full px-3 py-2 rounded-xl flex items-center justify-between hover:bg-sky-50 dark:hover:bg-white/5 transition-all font-semibold text-slate-700 dark:text-slate-200">
                <div class="flex items-center gap-2"><span>⚙️</span><span>Full System Settings</span></div>
                <span class="text-[10px] font-mono text-sky-600">Open</span>
              </button>
              <button onclick="toggleTheme()" class="w-full px-3 py-2 rounded-xl flex items-center justify-between hover:bg-slate-100 dark:hover:bg-white/5 transition-all font-semibold text-slate-700 dark:text-slate-200">
                <div class="flex items-center gap-2"><span>🌓</span><span id="themeMenuText">Toggle Theme</span></div>
                <span class="text-[10px] text-slate-400 font-mono">Appearance</span>
              </button>
              <a href="NUNES_FLEET_CLIENT_V7.zip" onclick="downloadFreshClientZip(event); toggleSettingsMenu();" class="w-full px-3 py-2 rounded-xl flex items-center justify-between bg-sky-600 hover:bg-sky-700 text-white font-bold transition-all shadow-sm">
                <div class="flex items-center gap-2"><span>📥</span><span>Download Client (.zip)</span></div>
                <span class="text-[10px] font-mono bg-white/20 px-1.5 py-0.5 rounded">ZIP</span>
              </a>
              <button onclick="checkForUpdates(); toggleSettingsMenu();" class="w-full px-3 py-2 rounded-xl flex items-center justify-between hover:bg-slate-100 dark:hover:bg-white/5 transition-all font-semibold text-slate-700 dark:text-slate-200">
                <div class="flex items-center gap-2"><span>🔄</span><span>Check OTA Updates</span></div>
                <span class="text-[10px] text-emerald-500 font-bold">OTA</span>
              </button>
              <button onclick="openAIChatModal(); toggleSettingsMenu();" class="w-full px-3 py-2 rounded-xl flex items-center justify-between hover:bg-slate-100 dark:hover:bg-white/5 transition-all font-semibold text-slate-700 dark:text-slate-200">
                <div class="flex items-center gap-2"><span>🤖</span><span>AI Technician Copilot</span></div>
                <span class="text-[10px] text-violet-500 font-bold">AI</span>
              </button>
            </div>
          </div>
        </div>

      </div>
    </header>

    <!-- 🌟 8 MAIN SECTIONS NAVIGATION TAB BAR -->
    <nav class="flex items-center gap-1 p-1 bg-sky-50/80 dark:bg-slate-900/80 rounded-2xl border border-sky-100 dark:border-sky-950/60 overflow-x-auto scrollbar-none" role="tablist">
      <button onclick="switchTab('overview')" id="tabBtn_overview" class="nav-tab-btn active" role="tab">
        <span>📊</span><span data-i18n="nav_overview">1. Overview</span>
      </button>
      <button onclick="switchTab('smart_scan')" id="tabBtn_smart_scan" class="nav-tab-btn" role="tab">
        <span>🔍</span><span data-i18n="nav_smart_scan">2. Smart Scan</span>
      </button>
      <button onclick="switchTab('diagnostics')" id="tabBtn_diagnostics" class="nav-tab-btn" role="tab">
        <span>🩺</span><span data-i18n="nav_diagnostics">3. AI Diagnostics</span>
      </button>
      <button onclick="switchTab('cleanup')" id="tabBtn_cleanup" class="nav-tab-btn" role="tab">
        <span>⚡</span><span data-i18n="nav_cleanup">4. Safe Cleanup</span>
      </button>
      <button onclick="switchTab('fleet')" id="tabBtn_fleet" class="nav-tab-btn" role="tab">
        <span>🖥️</span><span data-i18n="nav_fleet">5. Fleet Management</span>
      </button>
      <button onclick="switchTab('health')" id="tabBtn_health" class="nav-tab-btn" role="tab">
        <span>❤️</span><span data-i18n="nav_health">6. System Health</span>
      </button>
      <button onclick="switchTab('reports')" id="tabBtn_reports" class="nav-tab-btn" role="tab">
        <span>📋</span><span data-i18n="nav_reports">7. Reports</span>
      </button>
      <button onclick="switchTab('settings')" id="tabBtn_settings" class="nav-tab-btn" role="tab">
        <span>⚙️</span><span data-i18n="nav_settings">8. Settings</span>
      </button>
    </nav>
'''

print("Header and tab nav drafted successfully.")
