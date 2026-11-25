# -*- coding: utf-8 -*-
import sys
import os
import re
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

LIVE_SYNC_JS = """
    // 🌐 REAL-TIME FLEET SYNCHRONIZATION ENGINE (Global Live Node Tracker)
    let seenCleanTimestamps = new Set();
    let knownComputers = new Set(['DESKTOP-M378M07', 'DESKTOP-EV2F0TV', 'DESKTOP-I2MHDIB', 'DESKTOP-F8G3T2C']);

    async function pollLiveFleetStatus() {
      try {
        const res = await fetch('/api/status');
        if (!res.ok) return;
        const json = await res.json();
        const data = json.data || {};
        const fleet = data.fleet || [];

        // 1. Update global summary counters
        const nodesCountEl = document.getElementById('overviewNodesCount');
        if (nodesCountEl) nodesCountEl.textContent = `${fleet.length} Workstations`;

        const onlineBadgeEl = document.getElementById('overviewOnlineBadge');
        if (onlineBadgeEl) onlineBadgeEl.textContent = `${data.online_count || fleet.length} ONLINE`;

        const sidebarBadgeEl = document.getElementById('sidebarFleetCountBadge');
        if (sidebarBadgeEl) sidebarBadgeEl.textContent = fleet.length;

        const allBtn = document.getElementById('nodeBtn_all');
        if (allBtn) allBtn.textContent = `All Workstations (${fleet.length})`;

        const tfHealthEl = document.getElementById('tfHealthScore');
        if (tfHealthEl && data.online_count) {
          const score = ((data.online_count / fleet.length) * 100).toFixed(1);
          tfHealthEl.textContent = `${score}%`;
        }

        // 2. Process each fleet computer
        const grid = document.getElementById('fleetNodesDetailedGrid');

        fleet.forEach(node => {
          const pc = node.computer;
          if (!pc) return;

          let card = document.querySelector(`[data-node="${pc}"]`);

          // Check for clean event toast notification
          if (node.latest_result && (node.latest_result.timestamp || node.latest_result.TimestampUtc)) {
            const ts = node.latest_result.timestamp || node.latest_result.TimestampUtc;
            const tsKey = pc + '_' + ts;
            if (!seenCleanTimestamps.has(tsKey)) {
              seenCleanTimestamps.add(tsKey);
              const recMb = node.latest_result.recovered_mb || node.latest_result.ReclaimedMB || 0;
              if (seenCleanTimestamps.size > 1 && recMb > 0) {
                showToast(`⚡ ${pc} Auto-Clean: ${recMb} MB reclaimed!`, '✓');
              }
            }
          }

          if (card) {
            // Update existing card values
            const freeEl = card.querySelector('.node-free-space');
            if (freeEl && node.disk_free_gb !== undefined) {
              freeEl.textContent = `${node.disk_free_gb} GB`;
            }

            const statusEl = card.querySelector('.node-online-status');
            if (statusEl) {
              const isOnline = node.online !== false;
              const minsAgo = node.minutes_ago !== undefined ? node.minutes_ago.toFixed(1) + 'm' : '0.1m';
              statusEl.textContent = isOnline ? `ONLINE (${minsAgo})` : 'OFFLINE';
              statusEl.className = isOnline ?
                'node-online-status px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300' :
                'node-online-status px-2.5 py-1 rounded-full text-xs font-bold bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400';
            }
          } else if (grid) {
            // NEW COMPUTER CONNECTED FROM ANYWHERE IN THE WORLD! Dynamically build card!
            knownComputers.add(pc);
            const freeGb = node.disk_free_gb !== undefined ? node.disk_free_gb : '--';
            const ram = node.ram_load !== undefined ? node.ram_load : 52;
            const latency = node.disk_latency !== undefined ? node.disk_latency : '2.40';
            const minsAgo = node.minutes_ago !== undefined ? node.minutes_ago.toFixed(1) + 'm' : '0.1m';
            const netMode = node.network_mode || (node.tailscale_ip ? 'TAILSCALE' : 'OFFICE LAN');

            const newCard = document.createElement('div');
            newCard.setAttribute('data-node', pc);
            newCard.onclick = () => openNodeDetailDrawer(pc);
            newCard.className = 'surface-card rounded-2xl p-4 sm:p-5 space-y-3 cursor-pointer hover:border-sky-500 transition-all border border-sky-200 dark:border-white/10 animate-fade-in';
            newCard.innerHTML = `
              <div class="flex items-start justify-between">
                <div>
                  <div class="flex items-center gap-2">
                    <h4 class="font-bold text-sm text-slate-900 dark:text-white font-mono">${pc}</h4>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-sky-100 text-sky-800 dark:bg-sky-950/60 dark:text-sky-300">${netMode}</span>
                  </div>
                </div>
                <span class="node-online-status px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300">ONLINE (${minsAgo})</span>
              </div>

              <div class="grid grid-cols-3 gap-2 text-xs font-mono p-2.5 bg-slate-50 dark:bg-slate-900/60 rounded-xl">
                <div><span class="text-slate-400 block text-[10px]">Free Space</span><strong class="node-free-space text-slate-800 dark:text-slate-200">${freeGb} GB</strong></div>
                <div><span class="text-slate-400 block text-[10px]">RAM Load</span><strong class="text-amber-600">${ram}%</strong></div>
                <div><span class="text-slate-400 block text-[10px]">Disk Latency</span><strong class="text-emerald-600">${latency} ms</strong></div>
              </div>

              <div class="flex items-center justify-between pt-1">
                <span class="text-xs text-slate-500 font-mono">Version: <strong>v10.1 Enterprise</strong></span>
                <div class="flex items-center gap-2" onclick="event.stopPropagation()">
                  <button onclick="triggerDirectRescue('${pc}')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200 hover:bg-rose-100 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-800/40 transition-all">Rescue</button>
                  <button onclick="triggerDirectClean('${pc}')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-sky-600 text-white hover:bg-sky-700 transition-all shadow-sm">Safe Clean</button>
                </div>
              </div>
            `;
            grid.appendChild(newCard);

            // Add filter button
            const filterContainer = document.querySelector('#sec_fleet .flex.items-center.gap-2.overflow-x-auto');
            if (filterContainer && !document.getElementById(`nodeBtn_${pc}`)) {
              const btn = document.createElement('button');
              btn.id = `nodeBtn_${pc}`;
              btn.onclick = () => filterFleetByNode(pc);
              btn.className = 'px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono text-xs font-bold transition-all';
              btn.textContent = pc;
              filterContainer.appendChild(btn);
            }

            showToast(`🖥️ New Fleet Computer Connected: ${pc}!`, '🚀');
          }
        });
      } catch (err) {
        console.debug('Fleet poll status:', err);
      }
    }
"""

def patch_html_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add sidebarFleetCountBadge id to sidebar badge
    content = content.replace(
        '<span class="sidebar-text px-1.5 py-0.5 rounded-full text-[10px] font-mono bg-sky-100 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300 font-bold">4</span>',
        '<span id="sidebarFleetCountBadge" class="sidebar-text px-1.5 py-0.5 rounded-full text-[10px] font-mono bg-sky-100 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300 font-bold">4</span>'
    )

    # 2. Add helper classes to existing cards
    for pc, default_gb in [('DESKTOP-M378M07', '10.3 GB'), ('DESKTOP-EV2F0TV', '28.5 GB'), ('DESKTOP-I2MHDIB', '42.1 GB'), ('DESKTOP-F8G3T2C', '64.0 GB')]:
        # online badge
        old_online = f'<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">'
        new_online = f'<span class="node-online-status px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300">'
        # free space
        old_free = f'<div><span class="text-slate-400 block text-[10px]">Free Space</span><strong class="text-slate-800 dark:text-slate-200">{default_gb}</strong></div>'
        new_free = f'<div><span class="text-slate-400 block text-[10px]">Free Space</span><strong class="node-free-space text-slate-800 dark:text-slate-200">{default_gb}</strong></div>'
        
        content = content.replace(old_free, new_free)

    # Replace online badge generally in cards if not yet replaced
    content = re.sub(
        r'<span class="px-2\.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">ONLINE',
        r'<span class="node-online-status px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300">ONLINE',
        content
    )

    # 3. Add LIVE_SYNC_JS before DOMContentLoaded
    if 'function pollLiveFleetStatus()' not in content:
        content = content.replace(
            "window.addEventListener('DOMContentLoaded', () => {",
            LIVE_SYNC_JS + "\n    window.addEventListener('DOMContentLoaded', () => {"
        )

    # 4. Trigger pollLiveFleetStatus inside DOMContentLoaded
    if 'pollLiveFleetStatus();' not in content:
        content = content.replace(
            "refreshDiagnostics();",
            "refreshDiagnostics();\n      pollLiveFleetStatus();\n      setInterval(pollLiveFleetStatus, 3000);"
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath} with Live Fleet Sync Engine!")

if __name__ == '__main__':
    patch_html_file('index.html')
    patch_html_file('dashboard/templates/index.html')

    # Also update batch files to execute agent
    for bat in ['AUTONOMOUS_CACHE_CLEANER.bat', 'NUNES_CACHE_CLEANER.bat']:
        bat_content = f"""@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NUNES AUTONOMOUS FLEET - INSTANT CONNECT & CLEAN
color 0B
cls

echo ===============================================================================
echo       NUNES AUTONOMOUS FLEET - SAFE CLEAN & LIVE TELEMETRY (v10.1)
echo ===============================================================================
echo.
echo [*] Initializing safe clean & dashboard synchronization...
echo [*] Computer Name: %COMPUTERNAME%
echo.

if exist "%~dp0CONNECT_THIS_PC.bat" (
    call "%~dp0CONNECT_THIS_PC.bat" %*
    exit /b %errorlevel%
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0nunes_fleet_agent.ps1"
exit /b %errorlevel%
"""
        with open(bat, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        print(f"Updated {bat} to delegate to fleet connector.")
