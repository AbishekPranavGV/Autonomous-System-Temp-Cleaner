# -*- coding: utf-8 -*-
import sys
import os

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def update_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = [
        # Overview
        ('<span data-i18n="grouped_departments">4 Office Departments</span>', '<span data-i18n="grouped_departments">4 Office Workstations</span>'),
        ('<!-- Fleet Workstations Summary by Department (2 Cols) -->', '<!-- Fleet Workstations Summary (2 Cols) -->'),
        ('<!-- Department Workstations Grid & Live Console Row -->', '<!-- Fleet Workstations Grid & Live Console Row -->'),
        ('data-i18n="dept_hub_title">NUNES Office Computers by Department</h3>', 'data-i18n="dept_hub_title">NUNES Office Computers</h3>'),
        ('Department: Engineering & Lab (Host PC)', 'Engineering & Lab (Host PC)'),
        ('Department: Accounts & Finance', 'Accounts & Finance'),
        ('Department: Production & Quality', 'Production & Quality'),
        ('Department: Front Office & Sales', 'Front Office & Sales'),
        
        # Fleet management section
        ('data-i18n="fleet_sub">Secure management of authorized office PCs with real heartbeat monitoring and department grouping</p>', 'data-i18n="fleet_sub">Secure management of authorized office PCs with real heartbeat monitoring</p>'),
        ('<!-- Department Filter Pills -->', '<!-- Fleet Filter Pills -->'),
        ('<button onclick="filterFleetByDept(\'all\')" id="deptBtn_all" class="px-3 py-1.5 rounded-xl bg-sky-600 text-white shadow-sm">All Departments (4)</button>', '<button onclick="filterFleetByDept(\'all\')" id="deptBtn_all" class="px-3 py-1.5 rounded-xl bg-sky-600 text-white shadow-sm">All Workstations (4)</button>'),
        ('<p class="text-xs font-medium text-sky-600 dark:text-sky-400 mt-0.5">Department: Engineering & Lab</p>', '<p class="text-xs font-medium text-sky-600 dark:text-sky-400 mt-0.5">Engineering & Lab</p>'),
        ('<p class="text-xs font-medium text-indigo-600 dark:text-indigo-400 mt-0.5">Department: Accounts & Finance</p>', '<p class="text-xs font-medium text-indigo-600 dark:text-indigo-400 mt-0.5">Accounts & Finance</p>'),
        ('<p class="text-xs font-medium text-teal-600 dark:text-teal-400 mt-0.5">Department: Production & Quality</p>', '<p class="text-xs font-medium text-teal-600 dark:text-teal-400 mt-0.5">Production & Quality</p>'),
        ('<p class="text-xs font-medium text-amber-600 dark:text-amber-400 mt-0.5">Department: Front Office & Sales</p>', '<p class="text-xs font-medium text-amber-600 dark:text-amber-400 mt-0.5">Front Office & Sales</p>'),
        
        # I18N
        ('dept_hub_title: "NUNES Office Computers by Department",', 'dept_hub_title: "NUNES Office Computers",'),
        ('fleet_sub: "Secure management of authorized office PCs with real heartbeat monitoring and department grouping",', 'fleet_sub: "Secure management of authorized office PCs with real heartbeat monitoring",'),
        ('grouped_departments: "4 Office Departments",', 'grouped_departments: "4 Office Workstations",'),
        ('dept_hub_title: "துறை வாரியாக NUNES அலுவலக கணினிகள்",', 'dept_hub_title: "NUNES அலுவலக கணினிகள்",'),
        ('fleet_sub: "அங்கீகரிக்கப்பட்ட அலுவலக கணினிகளின் இதயத்துடிப்பு கண்காணிப்பு & துறை வாரியான மேலாண்மை",', 'fleet_sub: "அங்கீகரிக்கப்பட்ட அலுவலக கணினிகளின் இதயத்துடிப்பு கண்காணிப்பு & மேலாண்மை",'),
        ('grouped_departments: "4 அலுவலக துறைகள்",', 'grouped_departments: "4 அலுவலக பணிநிலையங்கள்",')
    ]

    for src, dst in replacements:
        if src in content:
            content = content.replace(src, dst)
            print(f"Applied replacement in {filepath}: {src[:35]} -> {dst[:35]}")

    # Add data-dept attributes to cards if not present
    if 'id="fleetNodesDetailedGrid"' in content:
        # Card 1
        content = content.replace(
            '<!-- PC 1: DESKTOP-M378M07 -->\n        <div class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 border-sky-300 dark:border-sky-800">',
            '<!-- PC 1: DESKTOP-M378M07 -->\n        <div data-dept="eng" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3 border-sky-300 dark:border-sky-800">'
        )
        # Card 2
        content = content.replace(
            '<!-- PC 2: DESKTOP-EV2F0TV -->\n        <div class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">',
            '<!-- PC 2: DESKTOP-EV2F0TV -->\n        <div data-dept="acct" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">'
        )
        # Card 3
        content = content.replace(
            '<!-- PC 3: DESKTOP-I2MHDIB -->\n        <div class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">',
            '<!-- PC 3: DESKTOP-I2MHDIB -->\n        <div data-dept="prod" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">'
        )
        # Card 4
        content = content.replace(
            '<!-- PC 4: DESKTOP-F8G3T2C -->\n        <div class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">',
            '<!-- PC 4: DESKTOP-F8G3T2C -->\n        <div data-dept="sales" class="surface-card rounded-2xl p-4 sm:p-5 space-y-3">'
        )

    # Add filterFleetByDept function if not defined
    if 'function filterFleetByDept' not in content:
        filter_func = """
function filterFleetByDept(dept) {
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
}
"""
        # Insert before exportMaintenanceReport
        if 'function exportMaintenanceReport()' in content:
            content = content.replace('function exportMaintenanceReport()', filter_func + '\nfunction exportMaintenanceReport()')
            print(f"Added filterFleetByDept to {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath} successfully")

if __name__ == '__main__':
    update_file('index.html')
    update_file('dashboard/templates/index.html')
    update_file('scratch/part3.html')
    update_file('scratch/part4.html')
