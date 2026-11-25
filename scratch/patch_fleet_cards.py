import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update filter pills
    old_pills = """      <!-- Fleet Filter Pills -->
      <div class="flex items-center gap-2 overflow-x-auto scrollbar-none text-xs font-bold">
        <button onclick="filterFleetByNode('all')" id="nodeBtn_all" class="px-3 py-1.5 rounded-xl bg-sky-600 text-white shadow-sm">All Workstations (4)</button>
        <button onclick="filterFleetByNode('DESKTOP-M378M07')" id="nodeBtn_DESKTOP-M378M07" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-M378M07</button>
        <button onclick="filterFleetByNode('DESKTOP-EV2F0TV')" id="nodeBtn_DESKTOP-EV2F0TV" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-EV2F0TV</button>
        <button onclick="filterFleetByNode('DESKTOP-I2MHDIB')" id="nodeBtn_DESKTOP-I2MHDIB" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-I2MHDIB</button>
        <button onclick="filterFleetByNode('DESKTOP-F8G3T2C')" id="nodeBtn_DESKTOP-F8G3T2C" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-F8G3T2C</button>
      </div>"""

    new_pills = """      <!-- Fleet Filter Pills -->
      <div class="flex items-center gap-2 overflow-x-auto scrollbar-none text-xs font-bold">
        <button onclick="filterFleetByNode('all')" id="nodeBtn_all" class="px-3 py-1.5 rounded-xl bg-sky-600 text-white shadow-sm transition-all">All Workstations (4)</button>
        <button onclick="filterFleetByNode('DESKTOP-M378M07')" id="nodeBtn_DESKTOP-M378M07" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 transition-all">Engineering &amp; Lab</button>
        <button onclick="filterFleetByNode('DESKTOP-EV2F0TV')" id="nodeBtn_DESKTOP-EV2F0TV" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 transition-all">Accounts &amp; Finance</button>
        <button onclick="filterFleetByNode('DESKTOP-I2MHDIB')" id="nodeBtn_DESKTOP-I2MHDIB" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 transition-all">Production &amp; Quality</button>
        <button onclick="filterFleetByNode('DESKTOP-F8G3T2C')" id="nodeBtn_DESKTOP-F8G3T2C" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 transition-all">Front Office &amp; Sales</button>
      </div>"""

    if old_pills in content:
        content = content.replace(old_pills, new_pills)
        print(f"Patched filter pills in {filepath}")
    else:
        print(f"Old filter pills not matched exactly in {filepath}")

    # 2. Add clean department names to the 4 cards
    # Card 1: DESKTOP-M378M07
    card1_old = """        <div data-node="DESKTOP-M378M07" onclick="openNodeDetailDrawer('DESKTOP-M378M07')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 border-sky-300 dark:border-sky-800 cursor-pointer hover:border-sky-500 transition-all">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white font-mono">DESKTOP-M378M07</h4>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-sky-100 text-sky-800">THIS PC (HOST)</span>
              </div>
                          </div>"""

    card1_new = """        <div data-node="DESKTOP-M378M07" onclick="openNodeDetailDrawer('DESKTOP-M378M07')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 border-sky-300 dark:border-sky-800 cursor-pointer hover:border-sky-500 transition-all">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white font-mono">DESKTOP-M378M07</h4>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-sky-100 text-sky-800">THIS PC (HOST)</span>
              </div>
              <p class="text-xs text-sky-600 dark:text-sky-400 font-semibold mt-0.5">Engineering &amp; Lab</p>
            </div>"""

    if card1_old in content:
        content = content.replace(card1_old, card1_new)
        print(f"Patched card 1 in {filepath}")
    else:
        print(f"Card 1 not matched in {filepath}")

    # Card 2: DESKTOP-EV2F0TV
    card2_old = """        <div data-node="DESKTOP-EV2F0TV" onclick="openNodeDetailDrawer('DESKTOP-EV2F0TV')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 cursor-pointer hover:border-sky-500 transition-all">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white font-mono">DESKTOP-EV2F0TV</h4>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-100 text-indigo-800">TAILSCALE</span>
              </div>
                          </div>"""

    card2_new = """        <div data-node="DESKTOP-EV2F0TV" onclick="openNodeDetailDrawer('DESKTOP-EV2F0TV')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 cursor-pointer hover:border-sky-500 transition-all">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white font-mono">DESKTOP-EV2F0TV</h4>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-100 text-indigo-800">TAILSCALE</span>
              </div>
              <p class="text-xs text-indigo-600 dark:text-indigo-400 font-semibold mt-0.5">Accounts &amp; Finance</p>
            </div>"""

    if card2_old in content:
        content = content.replace(card2_old, card2_new)
        print(f"Patched card 2 in {filepath}")
    else:
        print(f"Card 2 not matched in {filepath}")

    # Card 3: DESKTOP-I2MHDIB
    card3_old = """        <div data-node="DESKTOP-I2MHDIB" onclick="openNodeDetailDrawer('DESKTOP-I2MHDIB')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 cursor-pointer hover:border-sky-500 transition-all">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white font-mono">DESKTOP-I2MHDIB</h4>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-100 text-teal-800">TAILSCALE</span>
              </div>
                          </div>"""

    card3_new = """        <div data-node="DESKTOP-I2MHDIB" onclick="openNodeDetailDrawer('DESKTOP-I2MHDIB')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 cursor-pointer hover:border-sky-500 transition-all">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white font-mono">DESKTOP-I2MHDIB</h4>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-100 text-teal-800">TAILSCALE</span>
              </div>
              <p class="text-xs text-teal-600 dark:text-teal-400 font-semibold mt-0.5">Production &amp; Quality</p>
            </div>"""

    if card3_old in content:
        content = content.replace(card3_old, card3_new)
        print(f"Patched card 3 in {filepath}")
    else:
        print(f"Card 3 not matched in {filepath}")

    # Card 4: DESKTOP-F8G3T2C
    card4_old = """        <div data-node="DESKTOP-F8G3T2C" onclick="openNodeDetailDrawer('DESKTOP-F8G3T2C')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 cursor-pointer hover:border-sky-500 transition-all">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white font-mono">DESKTOP-F8G3T2C</h4>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800">OFFICE LAN</span>
              </div>
                          </div>"""

    card4_new = """        <div data-node="DESKTOP-F8G3T2C" onclick="openNodeDetailDrawer('DESKTOP-F8G3T2C')" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 cursor-pointer hover:border-sky-500 transition-all">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white font-mono">DESKTOP-F8G3T2C</h4>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800">OFFICE LAN</span>
              </div>
              <p class="text-xs text-amber-600 dark:text-amber-400 font-semibold mt-0.5">Front Office &amp; Sales</p>
            </div>"""

    if card4_old in content:
        content = content.replace(card4_old, card4_new)
        print(f"Patched card 4 in {filepath}")
    else:
        print(f"Card 4 not matched in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved {filepath}")

patch_file('index.html')
patch_file('dashboard/templates/index.html')
