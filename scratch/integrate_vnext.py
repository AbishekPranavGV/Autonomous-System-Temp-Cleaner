# -*- coding: utf-8 -*-
import sys
import os
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from build_enterprise_vnext import (
    HEADER_SEARCH_AND_NOTIFICATIONS,
    CLEANUP_WORKFLOW_MODAL_HTML,
    NODE_DETAIL_DRAWER_HTML
)
from gen_sidebar import generate_sidebar_html

SIDEBAR_HTML = generate_sidebar_html()

def update_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ensure body has flex container for sidebar
    # We want <body ...><div class="flex h-screen overflow-hidden bg-slate-50 dark:bg-slate-950 font-sans">
    # Sidebar goes on left, main content on right.
    if '<aside id="appSidebar"' not in content:
        # Wrap main container
        body_start = '<body class="bg-[#f8fafc] text-slate-800 dark:bg-[#0b1120] dark:text-slate-100 min-h-screen transition-colors duration-200 antialiased font-sans flex flex-col justify-between selection:bg-sky-500 selection:text-white">'
        
        new_body_start = """<body class="bg-[#f8fafc] text-slate-800 dark:bg-[#0b1120] dark:text-slate-100 min-h-screen transition-colors duration-200 antialiased font-sans selection:bg-sky-500 selection:text-white flex overflow-hidden">
  
  <!-- Left Collapsible Sidebar -->
""" + SIDEBAR_HTML + """

  <!-- Main Scrollable App Container -->
  <div id="mainAppScrollContainer" class="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto">
"""
        if body_start in content:
            content = content.replace(body_start, new_body_start)
            # Close mainAppScrollContainer before </body>
            content = content.replace('</body>', '  </div>\n</body>')
            print(f"Added sidebar and main scroll container to {filepath}")
        else:
            # Fallback regex for body tag
            content = re.sub(r'<body([^>]*)>', r'<body\1 flex overflow-hidden>\n' + SIDEBAR_HTML + r'\n<div id="mainAppScrollContainer" class="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto">', content, count=1)
            content = content.replace('</body>', '  </div>\n</body>')
            print(f"Added sidebar via regex to {filepath}")

    # 2. Add Global Search and Notification Center to Sticky Header
    if 'id="notificationCenterContainer"' not in content:
        header_target = '<!-- 📊 Dashboard Quick Button -->'
        if header_target in content:
            content = content.replace(header_target, HEADER_SEARCH_AND_NOTIFICATIONS + "\n\n        " + header_target)
            print(f"Added search and notification center to {filepath}")

    # 3. Add Hamburger Menu for Mobile Sidebar Toggle in Header
    hamburger_btn = """        <!-- Mobile Sidebar Toggle -->
        <button onclick="toggleMobileSidebar()" class="lg:hidden p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">
          <span class="text-base">☰</span>
        </button>
"""
    if 'toggleMobileSidebar()' not in content:
        brand_target = '<div class="flex items-center gap-2.5">'
        if brand_target in content:
            content = content.replace(brand_target, hamburger_btn + "\n        " + brand_target, 1)
            print(f"Added mobile hamburger button to {filepath}")

    # 4. Insert Modals (Cleanup Workflow & Node Detail Drawer) before </body>
    if 'id="cleanupWorkflowModal"' not in content:
        modals_combined = CLEANUP_WORKFLOW_MODAL_HTML + "\n" + NODE_DETAIL_DRAWER_HTML + "\n"
        content = content.replace('</body>', modals_combined + '\n</body>')
        print(f"Added cleanup workflow & node detail drawer modals to {filepath}")

    # 5. Connect Workstation Cards to Node Detail Drawer
    # In Detailed Fleet Cards Grid: Add onclick="openNodeDetailDrawer('...')" and cursor-pointer
    cards = [
        ('<!-- PC 1: DESKTOP-M378M07 -->\n        <div data-node="DESKTOP-M378M07" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 border-sky-300 dark:border-sky-800">',
         '<!-- PC 1: DESKTOP-M378M07 -->\n        <div data-node="DESKTOP-M378M07" onclick="openNodeDetailDrawer(\'DESKTOP-M378M07\')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 border-sky-300 dark:border-sky-800 cursor-pointer hover:border-sky-500 transition-all">'),
        ('<!-- PC 2: DESKTOP-EV2F0TV -->\n        <div data-node="DESKTOP-EV2F0TV" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">',
         '<!-- PC 2: DESKTOP-EV2F0TV -->\n        <div data-node="DESKTOP-EV2F0TV" onclick="openNodeDetailDrawer(\'DESKTOP-EV2F0TV\')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 cursor-pointer hover:border-sky-500 transition-all">'),
        ('<!-- PC 3: DESKTOP-I2MHDIB -->\n        <div data-node="DESKTOP-I2MHDIB" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">',
         '<!-- PC 3: DESKTOP-I2MHDIB -->\n        <div data-node="DESKTOP-I2MHDIB" onclick="openNodeDetailDrawer(\'DESKTOP-I2MHDIB\')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 cursor-pointer hover:border-sky-500 transition-all">'),
        ('<!-- PC 4: DESKTOP-F8G3T2C -->\n        <div data-node="DESKTOP-F8G3T2C" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">',
         '<!-- PC 4: DESKTOP-F8G3T2C -->\n        <div data-node="DESKTOP-F8G3T2C" onclick="openNodeDetailDrawer(\'DESKTOP-F8G3T2C\')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 cursor-pointer hover:border-sky-500 transition-all">')
    ]
    for old_c, new_c in cards:
        if old_c in content:
            content = content.replace(old_c, new_c)
            print(f"Hooked openNodeDetailDrawer for card in {filepath}")

    # 6. Enhance Reports Section with Multi-Format Export Buttons
    old_reports_export = '<button onclick="exportMaintenanceReport()" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-sky-600 hover:bg-sky-700 text-white shadow-sm flex items-center gap-1.5 active:scale-95 transition-all">'
    new_reports_export = """<div class="flex items-center gap-2">
            <button onclick="exportReport('csv')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition-all flex items-center gap-1">
              <span>📊</span><span>Export CSV</span>
            </button>
            <button onclick="exportReport('json')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-sky-600 hover:bg-sky-700 text-white shadow-sm flex items-center gap-1.5 active:scale-95 transition-all">
              <span>📄</span><span>Export JSON</span>
            </button>
            <button onclick="window.print()" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-indigo-50 hover:bg-indigo-100 text-indigo-700 dark:bg-indigo-950/40 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800/40 transition-all flex items-center gap-1">
              <span>🖨️</span><span>Print</span>
            </button>
          </div>"""
    if old_reports_export in content:
        content = content.replace(old_reports_export, new_reports_export + '\n          <button style="display:none;" onclick="exportMaintenanceReport()"')
        print(f"Enhanced Reports export controls in {filepath}")

    # 7. Add Enterprise JavaScript Handlers
    enterprise_js = """
    // 🌟 ENTERPRISE vNEXT CONTROLLERS (Sidebar, Search, Workflow, Node Inspector)
    let isSidebarCollapsed = false;
    let currentWorkflowStep = 1;
    let selectedWorkflowNode = 'DESKTOP-M378M07';

    function toggleSidebarCollapse() {
      const sidebar = document.getElementById('appSidebar');
      const icon = document.getElementById('collapseIcon');
      if (!sidebar) return;
      isSidebarCollapsed = !isSidebarCollapsed;
      if (isSidebarCollapsed) {
        sidebar.classList.remove('w-64');
        sidebar.classList.add('w-16');
        document.querySelectorAll('.sidebar-text').forEach(el => el.classList.add('hidden'));
        if (icon) icon.textContent = '▶';
      } else {
        sidebar.classList.remove('w-16');
        sidebar.classList.add('w-64');
        document.querySelectorAll('.sidebar-text').forEach(el => el.classList.remove('hidden'));
        if (icon) icon.textContent = '◀';
      }
    }

    function toggleMobileSidebar() {
      const sidebar = document.getElementById('appSidebar');
      if (!sidebar) return;
      sidebar.classList.toggle('hidden');
      sidebar.classList.toggle('fixed');
      sidebar.classList.toggle('inset-y-0');
      sidebar.classList.toggle('left-0');
      sidebar.classList.toggle('z-50');
      sidebar.classList.toggle('shadow-2xl');
    }

    function handleGlobalFleetSearch(q) {
      const query = q.toLowerCase().trim();
      const cards = document.querySelectorAll('#fleetNodesDetailedGrid > div, #overviewFleetGrid > div');
      cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (!query || text.includes(query)) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function toggleNotificationCenter(event) {
      if (event) event.stopPropagation();
      const panel = document.getElementById('notificationDropdownPanel');
      if (panel) panel.classList.toggle('hidden');
    }

    function clearNotifications() {
      const badge = document.getElementById('notificationBadgeCount');
      const list = document.getElementById('notificationItemsList');
      if (badge) badge.style.display = 'none';
      if (list) {
        list.innerHTML = '<div class="p-4 text-center text-slate-400 text-xs">All notifications marked as read.</div>';
      }
      showToast('Notifications marked as read', '✓');
    }

    // 4-Step Cleanup Workflow
    function openCleanupWorkflow(nodeName) {
      selectedWorkflowNode = nodeName || 'DESKTOP-M378M07';
      currentWorkflowStep = 1;
      updateCleanupWorkflowUI();
      const modal = document.getElementById('cleanupWorkflowModal');
      if (modal) modal.classList.remove('hidden');
    }

    function closeCleanupWorkflow() {
      const modal = document.getElementById('cleanupWorkflowModal');
      if (modal) modal.classList.add('hidden');
    }

    function updateCleanupWorkflowUI() {
      const stepNumEl = document.getElementById('cwStepNum');
      if (stepNumEl) stepNumEl.textContent = currentWorkflowStep;

      for (let i = 1; i <= 4; i++) {
        const tab = document.getElementById('cwStepTab' + i);
        const content = document.getElementById('cwStepContent' + i);
        if (tab) {
          if (i === currentWorkflowStep) {
            tab.className = 'py-2.5 bg-sky-600 text-white transition-all font-bold';
          } else if (i < currentWorkflowStep) {
            tab.className = 'py-2.5 bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-400 font-bold transition-all';
          } else {
            tab.className = 'py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 transition-all';
          }
        }
        if (content) {
          content.classList.toggle('hidden', i !== currentWorkflowStep);
        }
      }

      const prevBtn = document.getElementById('btnCwPrev');
      const nextBtn = document.getElementById('btnCwNext');
      if (prevBtn) prevBtn.classList.toggle('hidden', currentWorkflowStep === 1 || currentWorkflowStep === 4);
      if (nextBtn) {
        if (currentWorkflowStep === 1) nextBtn.textContent = 'Proceed to Review →';
        else if (currentWorkflowStep === 2) nextBtn.textContent = 'Authorize Action →';
        else if (currentWorkflowStep === 3) nextBtn.textContent = '⚡ Execute Verified Clean';
        else if (currentWorkflowStep === 4) nextBtn.textContent = 'Close & Return';
      }
    }

    function nextCleanupWorkflowStep() {
      if (currentWorkflowStep === 1) {
        currentWorkflowStep = 2;
        updateCleanupWorkflowUI();
      } else if (currentWorkflowStep === 2) {
        currentWorkflowStep = 3;
        updateCleanupWorkflowUI();
      } else if (currentWorkflowStep === 3) {
        const check = document.getElementById('cwAdminConfirmCheck');
        if (check && !check.checked) {
          showToast('Please check the authorization box to proceed', '⚠️');
          return;
        }
        triggerCleanSelected();
        currentWorkflowStep = 4;
        updateCleanupWorkflowUI();
      } else if (currentWorkflowStep === 4) {
        closeCleanupWorkflow();
      }
    }

    function prevCleanupWorkflowStep() {
      if (currentWorkflowStep > 1 && currentWorkflowStep < 4) {
        currentWorkflowStep--;
        updateCleanupWorkflowUI();
      }
    }

    // Workstation Deep Diagnostic Drawer
    let activeDrawerNode = 'DESKTOP-M378M07';
    function openNodeDetailDrawer(nodeName) {
      activeDrawerNode = nodeName;
      const drawer = document.getElementById('nodeDetailDrawer');
      const hEl = document.getElementById('ndDrawerHostname');
      const rEl = document.getElementById('ndDrawerRole');
      const fEl = document.getElementById('ndDrawerFree');
      const ramEl = document.getElementById('ndDrawerRam');
      const latEl = document.getElementById('ndDrawerLatency');
      const ipEl = document.getElementById('ndDrawerIp');

      if (hEl) hEl.textContent = nodeName;
      if (rEl) {
        if (nodeName.includes('M378')) rEl.textContent = 'Host PC (Direct Win32 Access)';
        else if (nodeName.includes('EV2F') || nodeName.includes('I2MH')) rEl.textContent = 'Tailscale Remote Mesh';
        else rEl.textContent = 'Office LAN Node';
      }

      if (nodeName.includes('M378')) {
        if (fEl) fEl.textContent = '10.3 GB';
        if (ramEl) ramEl.textContent = '78%';
        if (latEl) latEl.textContent = '2.15 ms';
        if (ipEl) ipEl.textContent = '127.0.0.1';
      } else if (nodeName.includes('EV2F')) {
        if (fEl) fEl.textContent = '28.5 GB';
        if (ramEl) ramEl.textContent = '65%';
        if (latEl) latEl.textContent = '3.10 ms';
        if (ipEl) ipEl.textContent = '100.95.82.12';
      } else if (nodeName.includes('I2MH')) {
        if (fEl) fEl.textContent = '42.1 GB';
        if (ramEl) ramEl.textContent = '58%';
        if (latEl) latEl.textContent = '2.80 ms';
        if (ipEl) ipEl.textContent = '100.84.19.44';
      } else {
        if (fEl) fEl.textContent = '64.0 GB';
        if (ramEl) ramEl.textContent = '52%';
        if (latEl) latEl.textContent = '4.10 ms';
        if (ipEl) ipEl.textContent = '192.168.1.140';
      }

      if (drawer) drawer.classList.remove('hidden');
    }

    function closeNodeDetailDrawer() {
      const drawer = document.getElementById('nodeDetailDrawer');
      if (drawer) drawer.classList.add('hidden');
    }

    function triggerDirectRescueFromDrawer() {
      triggerDirectRescue(activeDrawerNode);
      closeNodeDetailDrawer();
    }

    function triggerDirectCleanFromDrawer() {
      openCleanupWorkflow(activeDrawerNode);
      closeNodeDetailDrawer();
    }

    // Reports Multi-Format Export
    function exportReport(fmt) {
      if (fmt === 'csv') {
        window.open('/api/reports/export?format=csv', '_blank');
        showToast('Exported Fleet CSV Report', '📊');
      } else if (fmt === 'json') {
        window.open('/api/reports/export?format=json', '_blank');
        showToast('Exported Fleet JSON Report', '📄');
      } else {
        window.print();
      }
    }

    // Sync sidebar active state when switchTab runs
    const origSwitchTab = window.switchTab;
    window.switchTab = function(tabId) {
      if (origSwitchTab) origSwitchTab(tabId);
      document.querySelectorAll('.sidebar-nav-btn').forEach(b => {
        b.className = b.className.replace('bg-sky-50 text-sky-700 dark:bg-sky-950/60 dark:text-sky-300 font-bold', 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5');
      });
      const sideBtn = document.getElementById('sideBtn_' + tabId);
      if (sideBtn) {
        sideBtn.className = 'w-full flex items-center gap-3 px-3 py-2.5 rounded-xl bg-sky-50 text-sky-700 dark:bg-sky-950/60 dark:text-sky-300 font-bold transition-all sidebar-nav-btn active';
      }
    };

    // Close flyouts on outside click or Escape
    document.addEventListener('click', (e) => {
      const notifPanel = document.getElementById('notificationDropdownPanel');
      const notifBtn = document.getElementById('btnNotificationCenter');
      if (notifPanel && !notifPanel.classList.contains('hidden')) {
        if (!notifPanel.contains(e.target) && (!notifBtn || !notifBtn.contains(e.target))) {
          notifPanel.classList.add('hidden');
        }
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeCleanupWorkflow();
        closeNodeDetailDrawer();
        const notifPanel = document.getElementById('notificationDropdownPanel');
        if (notifPanel) notifPanel.classList.add('hidden');
      }
    });
"""

    if 'function toggleSidebarCollapse()' not in content:
        # Insert before exportMaintenanceReport
        target_fn = 'function exportMaintenanceReport()'
        if target_fn in content:
            content = content.replace(target_fn, enterprise_js + "\n" + target_fn)
            print(f"Added enterprise JavaScript controllers to {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully processed {filepath}")

if __name__ == '__main__':
    update_file('index.html')
    update_file('dashboard/templates/index.html')
