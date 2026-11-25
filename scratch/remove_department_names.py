# -*- coding: utf-8 -*-
import sys
import os

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def update_html_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Overview cards: remove the department subtitle lines
    overview_replaces = [
        ('<div class="text-[11px] font-semibold text-sky-700 dark:text-sky-400">Engineering & Lab (Host PC)</div>\n', ''),
        ('<div class="text-[11px] font-semibold text-sky-700 dark:text-sky-400">Engineering & Lab (Host PC)</div>\r\n', ''),
        ('<div class="text-[11px] font-semibold text-sky-700 dark:text-sky-400">Engineering & Lab (Host PC)</div>', ''),
        
        ('<div class="text-[11px] font-semibold text-indigo-700 dark:text-indigo-400">Accounts & Finance</div>\n', ''),
        ('<div class="text-[11px] font-semibold text-indigo-700 dark:text-indigo-400">Accounts & Finance</div>\r\n', ''),
        ('<div class="text-[11px] font-semibold text-indigo-700 dark:text-indigo-400">Accounts & Finance</div>', ''),
        
        ('<div class="text-[11px] font-semibold text-teal-700 dark:text-teal-400">Production & Quality</div>\n', ''),
        ('<div class="text-[11px] font-semibold text-teal-700 dark:text-teal-400">Production & Quality</div>\r\n', ''),
        ('<div class="text-[11px] font-semibold text-teal-700 dark:text-teal-400">Production & Quality</div>', ''),
        
        ('<div class="text-[11px] font-semibold text-amber-700 dark:text-amber-400">Front Office & Sales</div>\n', ''),
        ('<div class="text-[11px] font-semibold text-amber-700 dark:text-amber-400">Front Office & Sales</div>\r\n', ''),
        ('<div class="text-[11px] font-semibold text-amber-700 dark:text-amber-400">Front Office & Sales</div>', '')
    ]
    for src, dst in overview_replaces:
        content = content.replace(src, dst)

    # 2. Detailed fleet cards: remove the department subtitle paragraphs
    card_replaces = [
        ('<p class="text-xs font-medium text-sky-600 dark:text-sky-400 mt-0.5">Engineering & Lab</p>\n', ''),
        ('<p class="text-xs font-medium text-sky-600 dark:text-sky-400 mt-0.5">Engineering & Lab</p>\r\n', ''),
        ('<p class="text-xs font-medium text-sky-600 dark:text-sky-400 mt-0.5">Engineering & Lab</p>', ''),
        
        ('<p class="text-xs font-medium text-indigo-600 dark:text-indigo-400 mt-0.5">Accounts & Finance</p>\n', ''),
        ('<p class="text-xs font-medium text-indigo-600 dark:text-indigo-400 mt-0.5">Accounts & Finance</p>\r\n', ''),
        ('<p class="text-xs font-medium text-indigo-600 dark:text-indigo-400 mt-0.5">Accounts & Finance</p>', ''),
        
        ('<p class="text-xs font-medium text-teal-600 dark:text-teal-400 mt-0.5">Production & Quality</p>\n', ''),
        ('<p class="text-xs font-medium text-teal-600 dark:text-teal-400 mt-0.5">Production & Quality</p>\r\n', ''),
        ('<p class="text-xs font-medium text-teal-600 dark:text-teal-400 mt-0.5">Production & Quality</p>', ''),
        
        ('<p class="text-xs font-medium text-amber-600 dark:text-amber-400 mt-0.5">Front Office & Sales</p>\n', ''),
        ('<p class="text-xs font-medium text-amber-600 dark:text-amber-400 mt-0.5">Front Office & Sales</p>\r\n', ''),
        ('<p class="text-xs font-medium text-amber-600 dark:text-amber-400 mt-0.5">Front Office & Sales</p>', '')
    ]
    for src, dst in card_replaces:
        content = content.replace(src, dst)

    # 3. Filter pills: change buttons to filter by node name
    old_pills = """      <!-- Fleet Filter Pills -->
      <div class="flex items-center gap-2 overflow-x-auto scrollbar-none text-xs font-bold">
        <button onclick="filterFleetByDept('all')" id="deptBtn_all" class="px-3 py-1.5 rounded-xl bg-sky-600 text-white shadow-sm">All Workstations (4)</button>
        <button onclick="filterFleetByDept('eng')" id="deptBtn_eng" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600">Engineering & Lab</button>
        <button onclick="filterFleetByDept('acct')" id="deptBtn_acct" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600">Accounts & Finance</button>
        <button onclick="filterFleetByDept('prod')" id="deptBtn_prod" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600">Production & Quality</button>
        <button onclick="filterFleetByDept('sales')" id="deptBtn_sales" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600">Front Office & Sales</button>
      </div>"""

    new_pills = """      <!-- Fleet Filter Pills -->
      <div class="flex items-center gap-2 overflow-x-auto scrollbar-none text-xs font-bold">
        <button onclick="filterFleetByNode('all')" id="nodeBtn_all" class="px-3 py-1.5 rounded-xl bg-sky-600 text-white shadow-sm">All Workstations (4)</button>
        <button onclick="filterFleetByNode('DESKTOP-M378M07')" id="nodeBtn_DESKTOP-M378M07" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-M378M07</button>
        <button onclick="filterFleetByNode('DESKTOP-EV2F0TV')" id="nodeBtn_DESKTOP-EV2F0TV" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-EV2F0TV</button>
        <button onclick="filterFleetByNode('DESKTOP-I2MHDIB')" id="nodeBtn_DESKTOP-I2MHDIB" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-I2MHDIB</button>
        <button onclick="filterFleetByNode('DESKTOP-F8G3T2C')" id="nodeBtn_DESKTOP-F8G3T2C" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-F8G3T2C</button>
      </div>"""

    if old_pills in content:
        content = content.replace(old_pills, new_pills)
        print(f"Replaced filter pills in {filepath}")
    else:
        # Fallback line-by-line replacement for pills
        content = content.replace(
            '<button onclick="filterFleetByDept(\'eng\')" id="deptBtn_eng" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600">Engineering & Lab</button>',
            '<button onclick="filterFleetByNode(\'DESKTOP-M378M07\')" id="nodeBtn_DESKTOP-M378M07" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-M378M07</button>'
        )
        content = content.replace(
            '<button onclick="filterFleetByDept(\'acct\')" id="deptBtn_acct" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600">Accounts & Finance</button>',
            '<button onclick="filterFleetByNode(\'DESKTOP-EV2F0TV\')" id="nodeBtn_DESKTOP-EV2F0TV" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-EV2F0TV</button>'
        )
        content = content.replace(
            '<button onclick="filterFleetByDept(\'prod\')" id="deptBtn_prod" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600">Production & Quality</button>',
            '<button onclick="filterFleetByNode(\'DESKTOP-I2MHDIB\')" id="nodeBtn_DESKTOP-I2MHDIB" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-I2MHDIB</button>'
        )
        content = content.replace(
            '<button onclick="filterFleetByDept(\'sales\')" id="deptBtn_sales" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600">Front Office & Sales</button>',
            '<button onclick="filterFleetByNode(\'DESKTOP-F8G3T2C\')" id="nodeBtn_DESKTOP-F8G3T2C" class="px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono">DESKTOP-F8G3T2C</button>'
        )
        content = content.replace(
            '<button onclick="filterFleetByDept(\'all\')" id="deptBtn_all"',
            '<button onclick="filterFleetByNode(\'all\')" id="nodeBtn_all"'
        )

    # 4. Settings options
    content = content.replace(
        '<option value="DESKTOP-M378M07">DESKTOP-M378M07 (Engineering & Lab)</option>',
        '<option value="DESKTOP-M378M07">DESKTOP-M378M07 (Host PC)</option>'
    )
    content = content.replace(
        '<option value="DESKTOP-EV2F0TV">DESKTOP-EV2F0TV (Accounts & Finance)</option>',
        '<option value="DESKTOP-EV2F0TV">DESKTOP-EV2F0TV (Tailscale Node)</option>'
    )
    content = content.replace(
        '<option value="DESKTOP-I2MHDIB">DESKTOP-I2MHDIB (Production & Quality)</option>',
        '<option value="DESKTOP-I2MHDIB">DESKTOP-I2MHDIB (Tailscale Node)</option>'
    )
    content = content.replace(
        '<option value="DESKTOP-F8G3T2C">DESKTOP-F8G3T2C (Front Office & Sales)</option>',
        '<option value="DESKTOP-F8G3T2C">DESKTOP-F8G3T2C (Office LAN Node)</option>'
    )

    # 5. Card data-node attributes
    content = content.replace('data-dept="eng"', 'data-node="DESKTOP-M378M07"')
    content = content.replace('data-dept="acct"', 'data-node="DESKTOP-EV2F0TV"')
    content = content.replace('data-dept="prod"', 'data-node="DESKTOP-I2MHDIB"')
    content = content.replace('data-dept="sales"', 'data-node="DESKTOP-F8G3T2C"')

    # 6. Comments in HTML
    content = content.replace('<!-- Node 1: Engineering & Lab -->', '<!-- Node 1: DESKTOP-M378M07 (Host) -->')
    content = content.replace('<!-- Node 2: Accounts & Finance -->', '<!-- Node 2: DESKTOP-EV2F0TV -->')
    content = content.replace('<!-- Node 3: Production & Quality -->', '<!-- Node 3: DESKTOP-I2MHDIB -->')
    content = content.replace('<!-- Node 4: Front Office & Sales -->', '<!-- Node 4: DESKTOP-F8G3T2C -->')

    # 7. Update filter function in JS
    old_filter_func = """function filterFleetByDept(dept) {
  const btns = ['all', 'eng', 'acct', 'prod', 'sales'];
  btns.forEach(b => {
    const el = document.getElementById('deptBtn_' + b);
    if (el) {
      if (b === dept) {
        el.className = 'px-3 py-1.5 rounded-xl bg-sky-600 text-white shadow-sm';
      } else {
        el.className = 'px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600';
      }
    }
  });
  const cards = document.querySelectorAll('#fleetNodesDetailedGrid > div');
  cards.forEach(card => {
    const cardDept = card.getAttribute('data-dept');
    if (dept === 'all' || cardDept === dept) {
      card.style.display = '';
    } else {
      card.style.display = 'none';
    }
  });
}"""

    new_filter_func = """function filterFleetByNode(nodeName) {
  const nodes = ['all', 'DESKTOP-M378M07', 'DESKTOP-EV2F0TV', 'DESKTOP-I2MHDIB', 'DESKTOP-F8G3T2C'];
  nodes.forEach(n => {
    const el = document.getElementById('nodeBtn_' + n);
    if (el) {
      if (n === nodeName) {
        el.className = 'px-3 py-1.5 rounded-xl bg-sky-600 text-white shadow-sm font-mono';
      } else {
        el.className = 'px-3 py-1.5 rounded-xl surface-card text-slate-600 hover:text-sky-600 font-mono';
      }
    }
  });
  const cards = document.querySelectorAll('#fleetNodesDetailedGrid > div');
  cards.forEach(card => {
    const cardNode = card.getAttribute('data-node');
    if (nodeName === 'all' || cardNode === nodeName) {
      card.style.display = '';
    } else {
      card.style.display = 'none';
    }
  });
}
window.filterFleetByDept = filterFleetByNode;"""

    if old_filter_func in content:
        content = content.replace(old_filter_func, new_filter_func)
        print(f"Updated filter function in {filepath}")

    # 8. exportMaintenanceReport nodes
    content = content.replace(
        '{ node: "DESKTOP-M378M07", department: "Engineering & Lab", status: "ONLINE", free_gb: 10.3 },',
        '{ node: "DESKTOP-M378M07", role: "Host PC", status: "ONLINE", free_gb: 10.3 },'
    )
    content = content.replace(
        '{ node: "DESKTOP-EV2F0TV", department: "Accounts & Finance", status: "ONLINE", free_gb: 28.5 },',
        '{ node: "DESKTOP-EV2F0TV", role: "Tailscale Node", status: "ONLINE", free_gb: 28.5 },'
    )
    content = content.replace(
        '{ node: "DESKTOP-I2MHDIB", department: "Production & Quality", status: "ONLINE", free_gb: 42.1 },',
        '{ node: "DESKTOP-I2MHDIB", role: "Tailscale Node", status: "ONLINE", free_gb: 42.1 },'
    )
    content = content.replace(
        '{ node: "DESKTOP-F8G3T2C", department: "Front Office & Sales", status: "ONLINE", free_gb: 64.0 }',
        '{ node: "DESKTOP-F8G3T2C", role: "Office LAN Node", status: "ONLINE", free_gb: 64.0 }'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {filepath}")

def update_app_py(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("'DESKTOP-M378M07': 'Engineering & Lab',", "'DESKTOP-M378M07': 'Host PC',")
    content = content.replace("'DESKTOP-EV2F0TV': 'Accounts & Finance',", "'DESKTOP-EV2F0TV': 'Tailscale Node',")
    content = content.replace("'DESKTOP-I2MHDIB': 'Production & Quality',", "'DESKTOP-I2MHDIB': 'Tailscale Node',")
    content = content.replace("'DESKTOP-F8G3T2C': 'Front Office & Sales'", "'DESKTOP-F8G3T2C': 'Office LAN Node'")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {filepath}")

if __name__ == '__main__':
    update_html_file('index.html')
    update_html_file('dashboard/templates/index.html')
    update_html_file('scratch/part3.html')
    update_html_file('scratch/part4.html')
    update_app_py('dashboard/app.py')
