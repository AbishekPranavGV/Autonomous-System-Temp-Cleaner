# -*- coding: utf-8 -*-
import sys
import os
import re
import subprocess
import tempfile

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def patch_file(filepath):
    print(f"Processing {filepath}...")
    if not os.path.exists(filepath):
        print(f"Error: {filepath} does not exist.")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix body tag (flex overflow-hidden inside class, remove body padding)
    content = re.sub(
        r'<body[^>]*flex\s+overflow-hidden>',
        '<body class="h-screen w-screen overflow-hidden flex bg-slate-100 dark:bg-slate-950 text-slate-800 dark:text-slate-100 font-sans antialiased selection:bg-sky-500 selection:text-white">',
        content
    )

    # 2. Add Mobile Backdrop right before or after sidebar
    if '<div id="mobileSidebarBackdrop"' not in content:
        backdrop_html = '\n  <!-- Mobile Sidebar Backdrop Overlay -->\n  <div id="mobileSidebarBackdrop" onclick="toggleMobileSidebar()" class="hidden fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-40 lg:hidden"></div>\n'
        content = content.replace('<!-- Left Collapsible Sidebar -->', backdrop_html + '  <!-- Left Collapsible Sidebar -->')
        # If not found via comment, try after <aside id="appSidebar" ... </aside>
        if '<div id="mobileSidebarBackdrop"' not in content:
            content = content.replace('</aside>', '</aside>\n  <div id="mobileSidebarBackdrop" onclick="toggleMobileSidebar()" class="hidden fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-40 lg:hidden"></div>')

    # 3. Fix mainAppScrollContainer padding and background
    content = re.sub(
        r'<div id="mainAppScrollContainer"[^>]*>',
        '<div id="mainAppScrollContainer" class="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto overflow-x-hidden p-2 sm:p-4 lg:p-6 bg-slate-50/50 dark:bg-slate-950/50">',
        content
    )

    # 4. Enhance app-window container
    content = content.replace(
        '<div class="w-full max-w-[99%] 2xl:max-w-[1680px] mx-auto app-window rounded-2xl sm:rounded-3xl p-3 sm:p-4 md:p-5 space-y-3 sm:space-y-4 transition-all duration-300">',
        '<div class="w-full max-w-[1680px] mx-auto app-window rounded-2xl sm:rounded-3xl p-3 sm:p-5 md:p-6 space-y-4 transition-all duration-300 shadow-xl shadow-sky-500/5">'
    )

    # 5. Add mobile menu button to Brand Area if not present
    hamburger_btn = '<button onclick="toggleMobileSidebar()" class="lg:hidden p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all flex items-center justify-center shrink-0" title="Toggle Navigation Menu"><span class="text-base leading-none">☰</span></button>'
    if 'toggleMobileSidebar()' not in content.split('</header>')[0]:
        brand_anchor = '<!-- Brand Area: NUNES AI PC Command Center v10.0 -->'
        if brand_anchor in content:
            content = content.replace(
                brand_anchor + '\n      <div class="flex items-center gap-3">',
                brand_anchor + '\n      <div class="flex items-center gap-2.5 sm:gap-3">\n        ' + hamburger_btn
            )

    # 6. Update Live Clock HTML to IST / Coimbatore
    old_clock = '<span id="liveStatusClock">LIVE • 17:25 UTC</span>'
    new_clock = '<span id="liveStatusClock">LIVE • --:--:-- IST</span>'
    content = content.replace(old_clock, new_clock)
    
    # Update clock container title
    content = content.replace(
        '<!-- Live Real-Time Heartbeat Clock -->\n        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-sky-50 dark:bg-sky-950/50 text-sky-700 dark:text-sky-300 border border-sky-200 dark:border-sky-800/80 text-xs font-mono font-bold shadow-sm">',
        '<!-- Live Real-Time Heartbeat Clock (Coimbatore, India - IST) -->\n        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-sky-50 dark:bg-sky-950/50 text-sky-700 dark:text-sky-300 border border-sky-200 dark:border-sky-800/80 text-xs font-mono font-bold shadow-sm shrink-0" title="Live Fleet Synchronization Time — Indian Standard Time (IST / Coimbatore, India - UTC+5:30)">'
    )

    # 7. Hide redundant header dashboard button (sidebar already has 1. Dashboard)
    content = re.sub(
        r'<button onclick="switchTab\(\'overview\'\)" id="btnHeaderDashboard"[^>]*>.*?</button>',
        '<button onclick="switchTab(\'overview\')" id="btnHeaderDashboard" style="display:none;"></button>',
        content,
        flags=re.DOTALL
    )

    # 8. Adjust Search Bar width so all header controls fit seamlessly on one line
    content = re.sub(
        r'<div class="relative flex-1 max-w-xs sm:max-w-sm hidden md:block">\s*<input type="text" id="globalFleetSearch"',
        '<div class="relative w-36 sm:w-44 lg:w-52 hidden sm:block shrink-0">\n          <input type="text" id="globalFleetSearch"',
        content
    )

    # 9. Update static notification timestamps from UTC to IST
    content = content.replace('>10:04 UTC<', '>15:34 IST<')
    content = content.replace('>10:00 UTC<', '>15:30 IST<')
    content = content.replace('>04:00 UTC<', '>09:30 IST<')
    content = content.replace('Timestamp (UTC)', 'Timestamp (IST)')
    content = content.replace('10:30:15 UTC', '16:00:15 IST')
    content = content.replace('03:45:22 UTC', '09:15:22 IST')

    # 10. Update JavaScript updateClock function to real IST (Asia/Kolkata / Coimbatore)
    old_update_clock = """    // Live clock update
    function updateClock() {
      const now = new Date();
      const hrs = String(now.getUTCHours()).padStart(2, '0');
      const mins = String(now.getUTCMinutes()).padStart(2, '0');
      const secs = String(now.getUTCSeconds()).padStart(2, '0');
      const el = document.getElementById('liveStatusClock');
      if (el) el.textContent = `LIVE • ${hrs}:${mins}:${secs} UTC`;
    }"""

    new_update_clock = """    // Live clock update (Indian Standard Time - Coimbatore, IST / UTC+5:30)
    function updateClock() {
      try {
        const now = new Date();
        const istFormatter = new Intl.DateTimeFormat('en-GB', {
          timeZone: 'Asia/Kolkata',
          hour12: false,
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        });
        const istTime = istFormatter.format(now);
        const el = document.getElementById('liveStatusClock');
        if (el) el.textContent = `LIVE • ${istTime} IST`;
      } catch (e) {
        const now = new Date();
        const istOffset = 5.5 * 60 * 60 * 1000;
        const istDate = new Date(now.getTime() + istOffset + (now.getTimezoneOffset() * 60 * 1000));
        const hrs = String(istDate.getHours()).padStart(2, '0');
        const mins = String(istDate.getMinutes()).padStart(2, '0');
        const secs = String(istDate.getSeconds()).padStart(2, '0');
        const el = document.getElementById('liveStatusClock');
        if (el) el.textContent = `LIVE • ${hrs}:${mins}:${secs} IST`;
      }
    }"""

    if old_update_clock in content:
        content = content.replace(old_update_clock, new_update_clock)
    else:
        # Fallback regex replace for updateClock
        content = re.sub(
            r'function updateClock\(\)\s*\{.*?if\s*\(el\)\s*el\.textContent\s*=\s*`LIVE\s*•\s*\$\{hrs\}:\$\{mins\}:\$\{secs\}\s*UTC`;\s*\}',
            new_update_clock.strip(),
            content,
            flags=re.DOTALL
        )

    # 11. Enhance toggleMobileSidebar in JS to handle backdrop and body lock
    old_toggle_mobile = """    function toggleMobileSidebar() {
      const sidebar = document.getElementById('appSidebar');
      if (!sidebar) return;
      sidebar.classList.toggle('hidden');
      sidebar.classList.toggle('fixed');
      sidebar.classList.toggle('inset-y-0');
      sidebar.classList.toggle('left-0');
      sidebar.classList.toggle('z-50');
      sidebar.classList.toggle('shadow-2xl');
    }"""

    new_toggle_mobile = """    function toggleMobileSidebar() {
      const sidebar = document.getElementById('appSidebar');
      const backdrop = document.getElementById('mobileSidebarBackdrop');
      if (!sidebar) return;
      const isMobileOpen = !sidebar.classList.contains('hidden') && sidebar.classList.contains('fixed');
      if (isMobileOpen) {
        sidebar.classList.add('hidden');
        sidebar.classList.remove('fixed', 'inset-y-0', 'left-0', 'z-50', 'shadow-2xl');
        if (backdrop) backdrop.classList.add('hidden');
      } else {
        sidebar.classList.remove('hidden');
        sidebar.classList.add('fixed', 'inset-y-0', 'left-0', 'z-50', 'shadow-2xl');
        if (backdrop) backdrop.classList.remove('hidden');
      }
    }"""

    if old_toggle_mobile in content:
        content = content.replace(old_toggle_mobile, new_toggle_mobile)

    # 12. Close mobile drawer on switchTab
    old_switch_tab = """    window.switchTab = function(tabId) {
      if (origSwitchTab) origSwitchTab(tabId);
      document.querySelectorAll('.sidebar-nav-btn').forEach(b => {
        b.className = b.className.replace('bg-sky-50 text-sky-700 dark:bg-sky-950/60 dark:text-sky-300 font-bold', 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5');
      });
      const sideBtn = document.getElementById('sideBtn_' + tabId);
      if (sideBtn) {
        sideBtn.className = 'w-full flex items-center gap-3 px-3 py-2.5 rounded-xl bg-sky-50 text-sky-700 dark:bg-sky-950/60 dark:text-sky-300 font-bold transition-all sidebar-nav-btn active';
      }
    };"""

    new_switch_tab = """    window.switchTab = function(tabId) {
      if (origSwitchTab) origSwitchTab(tabId);
      document.querySelectorAll('.sidebar-nav-btn').forEach(b => {
        b.className = b.className.replace('bg-sky-50 text-sky-700 dark:bg-sky-950/60 dark:text-sky-300 font-bold', 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5');
      });
      const sideBtn = document.getElementById('sideBtn_' + tabId);
      if (sideBtn) {
        sideBtn.className = 'w-full flex items-center gap-3 px-3 py-2.5 rounded-xl bg-sky-50 text-sky-700 dark:bg-sky-950/60 dark:text-sky-300 font-bold transition-all sidebar-nav-btn active';
      }
      if (window.innerWidth < 1024) {
        const sidebar = document.getElementById('appSidebar');
        const backdrop = document.getElementById('mobileSidebarBackdrop');
        if (sidebar && sidebar.classList.contains('fixed')) {
          sidebar.classList.add('hidden');
          sidebar.classList.remove('fixed', 'inset-y-0', 'left-0', 'z-50', 'shadow-2xl');
          if (backdrop) backdrop.classList.add('hidden');
        }
      }
    };"""

    if old_switch_tab in content:
        content = content.replace(old_switch_tab, new_switch_tab)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {filepath} successfully.")
    return True

if __name__ == '__main__':
    patch_file('index.html')
    patch_file('dashboard/templates/index.html')
