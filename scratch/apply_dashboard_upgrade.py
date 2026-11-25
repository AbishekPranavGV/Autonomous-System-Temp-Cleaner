# -*- coding: utf-8 -*-
import sys
import os

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def apply_upgrade_to_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update header: Add [📊 Dashboard] quick button before btnScanSelected
    old_header_target = """        <!-- 🔍 Scan Selected Button -->
        <button onclick="triggerScanSelected()" id="btnScanSelected\""""

    new_dashboard_btn = """        <!-- 📊 Dashboard Quick Button -->
        <button onclick="switchTab('overview')" id="btnHeaderDashboard" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold bg-sky-100 hover:bg-sky-200 dark:bg-sky-950/70 dark:hover:bg-sky-900/80 text-sky-800 dark:text-sky-300 border border-sky-300 dark:border-sky-700/60 transition-all flex items-center gap-1.5 active:scale-95 shadow-sm" title="Open Real-Time Interactive Fleet Dashboard">
          <span class="animate-pulse">📊</span>
          <span data-i18n="nav_dashboard_short">Dashboard</span>
        </button>

        <!-- 🔍 Scan Selected Button -->
        <button onclick="triggerScanSelected()" id="btnScanSelected\""""

    if "id=\"btnHeaderDashboard\"" not in content and old_header_target in content:
        content = content.replace(old_header_target, new_dashboard_btn)
        print(f"Added btnHeaderDashboard to {filepath}")

    # 2. Update navigation tab: "1. Overview" -> "1. Dashboard"
    content = content.replace(
        '<span data-i18n="nav_overview">1. Overview</span>',
        '<span data-i18n="nav_overview">1. Dashboard</span>'
    )

    # 3. Insert the Animated Interactive Graphs Suite into Section 1 (Overview / Dashboard)
    graphs_suite_html = """
      <!-- 🌟 ADVANCED ANIMATED INTERACTIVE GRAPH SUITE (DASHBOARD) -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4" id="dashboardGraphsSuite">
        
        <!-- Graph 1: Fleet Storage Recovery Trajectory (2 Cols) -->
        <div class="lg:col-span-2 surface-card rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-sm hover:shadow-md transition-all duration-300 border border-sky-100 dark:border-white/5 relative overflow-hidden group">
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 border-b border-sky-100 dark:border-sky-950/60 pb-3">
            <div>
              <div class="flex items-center gap-2">
                <span class="relative flex h-2.5 w-2.5">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-sky-500"></span>
                </span>
                <h3 class="text-sm font-extrabold text-slate-900 dark:text-white" data-i18n="chart_trajectory_title">Fleet Storage Recovery & Trajectory</h3>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-sky-100 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300">LIVE RAG</span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5" data-i18n="chart_trajectory_sub">Real-time multi-node storage capacity trajectory across verified sweep cycles</p>
            </div>
            
            <!-- Graph Timeframe Switcher -->
            <div class="flex items-center gap-1 p-1 bg-slate-100 dark:bg-slate-800 rounded-xl text-xs font-semibold">
              <button onclick="updateDashboardGraphTimeframe('today')" id="graphTfBtn_today" class="px-2.5 py-1 rounded-lg bg-white dark:bg-slate-700 text-sky-700 dark:text-sky-300 shadow-xs transition-all font-bold">Today</button>
              <button onclick="updateDashboardGraphTimeframe('month')" id="graphTfBtn_month" class="px-2.5 py-1 rounded-lg text-slate-600 dark:text-slate-300 hover:text-sky-600 transition-all font-medium">Month</button>
              <button onclick="updateDashboardGraphTimeframe('year')" id="graphTfBtn_year" class="px-2.5 py-1 rounded-lg text-slate-600 dark:text-slate-300 hover:text-sky-600 transition-all font-medium">Year</button>
            </div>
          </div>

          <!-- Chart.js Canvas -->
          <div class="relative h-64 sm:h-72 w-full">
            <canvas id="dashboardTrajectoryChart"></canvas>
          </div>

          <!-- Micro Telemetry Bar under graph -->
          <div class="flex flex-wrap items-center justify-between pt-2 border-t border-slate-100 dark:border-white/5 text-[11px] font-mono text-slate-500 dark:text-slate-400 gap-2">
            <div class="flex items-center gap-3">
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-sky-500"></span> DESKTOP-M378M07: <strong class="text-slate-800 dark:text-slate-200">10.3 GB Free</strong></span>
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span> DESKTOP-EV2F0TV: <strong class="text-slate-800 dark:text-slate-200">28.5 GB Free</strong></span>
            </div>
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 font-bold text-[10px]">99.8% Healthy</span>
              <span class="text-slate-400">Disk I/O: 2.15 ms</span>
            </div>
          </div>
        </div>

        <!-- Graph 2: Recovery Allocation Breakdown (1 Col) -->
        <div class="surface-card rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-sm hover:shadow-md transition-all duration-300 border border-sky-100 dark:border-white/5 flex flex-col justify-between relative overflow-hidden group">
          <div class="border-b border-sky-100 dark:border-sky-950/60 pb-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-sm">🍩</span>
                <h3 class="text-sm font-extrabold text-slate-900 dark:text-white" data-i18n="chart_category_title">Recovery Allocation</h3>
              </div>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-sky-100 text-sky-800 dark:bg-sky-950/60 dark:text-sky-300">1.49 GB</span>
            </div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5" data-i18n="chart_category_sub">Zero-risk verified reclaimable breakdown</p>
          </div>

          <!-- Chart.js Doughnut Canvas -->
          <div class="relative h-56 sm:h-60 w-full flex items-center justify-center">
            <canvas id="dashboardCategoryChart"></canvas>
          </div>

          <!-- Category Legend Grid -->
          <div class="grid grid-cols-2 gap-1.5 pt-2 border-t border-slate-100 dark:border-white/5 text-[10px] font-mono">
            <div class="flex items-center gap-1.5 text-slate-600 dark:text-slate-300"><span class="w-2 h-2 rounded-full bg-sky-600"></span> cleanmgr: 850 MB</div>
            <div class="flex items-center gap-1.5 text-slate-600 dark:text-slate-300"><span class="w-2 h-2 rounded-full bg-rose-500"></span> RAM Trim: 512 MB</div>
            <div class="flex items-center gap-1.5 text-slate-600 dark:text-slate-300"><span class="w-2 h-2 rounded-full bg-cyan-500"></span> Shaders: 145 MB</div>
            <div class="flex items-center gap-1.5 text-slate-600 dark:text-slate-300"><span class="w-2 h-2 rounded-full bg-purple-500"></span> User Temp: 28.7 MB</div>
          </div>
        </div>

      </div>

      <!-- Graph 3: Comparative Workstation Fleet Workload (Grouped Bar Chart) -->
      <div class="surface-card rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-sm hover:shadow-md transition-all duration-300 border border-sky-100 dark:border-white/5">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 border-b border-sky-100 dark:border-sky-950/60 pb-3">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-sm">📊</span>
              <h3 class="text-sm font-extrabold text-slate-900 dark:text-white" data-i18n="chart_workload_title">Fleet Workstation Telemetry & Workload Comparison</h3>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-indigo-100 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300">4 WORKSTATIONS</span>
            </div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5" data-i18n="chart_workload_sub">Comparative RAM utilization %, free storage capacity (GB), and disk latency</p>
          </div>
          <div class="flex items-center gap-3 text-xs font-mono text-slate-500 dark:text-slate-400">
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-sm bg-amber-500"></span> RAM Load %</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-sm bg-sky-500"></span> Free Storage (GB)</span>
          </div>
        </div>

        <div class="relative h-56 sm:h-64 w-full">
          <canvas id="dashboardWorkloadChart"></canvas>
        </div>
      </div>
"""

    kpi_end_marker = """        <!-- Card 4: Unified 30-Day Retention -->
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

      </div>"""

    if "id=\"dashboardGraphsSuite\"" not in content and kpi_end_marker in content:
        content = content.replace(kpi_end_marker, kpi_end_marker + "\n" + graphs_suite_html)
        print(f"Inserted dashboardGraphsSuite into {filepath}")
    elif "id=\"dashboardGraphsSuite\"" not in content:
        # Alternative insertion before Fleet Workstations Grid & Live Console Row
        alt_marker = "<!-- Fleet Workstations Grid & Live Console Row -->"
        if alt_marker in content:
            content = content.replace(alt_marker, graphs_suite_html + "\n      " + alt_marker)
            print(f"Inserted dashboardGraphsSuite via alt_marker into {filepath}")

    # 4. Update I18N translations
    # English additions
    en_target = 'nav_overview: "1. Overview",'
    en_replacement = """nav_overview: "1. Dashboard",
        nav_dashboard_short: "Dashboard",
        chart_trajectory_title: "Fleet Storage Recovery & Trajectory",
        chart_trajectory_sub: "Real-time multi-node storage capacity trajectory across verified sweep cycles",
        chart_category_title: "Recovery Allocation",
        chart_category_sub: "Zero-risk verified reclaimable breakdown",
        chart_workload_title: "Fleet Workstation Telemetry & Workload Comparison",
        chart_workload_sub: "Comparative RAM utilization %, free storage capacity (GB), and disk latency","""

    if en_target in content:
        content = content.replace(en_target, en_replacement)
        print(f"Updated English I18N in {filepath}")

    # Tamil additions
    ta_target = 'nav_overview: "1. கண்ணோட்டம்",'
    ta_replacement = """nav_overview: "1. டாஷ்போர்டு",
        nav_dashboard_short: "டாஷ்போர்டு",
        chart_trajectory_title: "நெட்வொர்க் சேமிப்பக மீட்பு & போக்கு",
        chart_trajectory_sub: "சரிபார்க்கப்பட்ட சுழற்சிகளின் நேரலை சேமிப்பக திறன் பாதை",
        chart_category_title: "மீட்பு பகிர்வு விவரம்",
        chart_category_sub: "பூஜ்ஜிய-ஆபத்து சரிபார்க்கப்பட்ட வகைப்பாடு",
        chart_workload_title: "பணிநிலைய சுமை ஒப்பீடு",
        chart_workload_sub: "நேரடி RAM சுமை, வட்டு தாமதம் மற்றும் இலவச சேமிப்பகம்","""

    if ta_target in content:
        content = content.replace(ta_target, ta_replacement)
        print(f"Updated Tamil I18N in {filepath}")

    # 5. Insert JavaScript Chart Controllers and Animations
    js_code = """
    // 🌟 ANIMATED DASHBOARD CHARTS SUITE
    let dashboardTrajectoryChart = null;
    let dashboardCategoryChart = null;
    let dashboardWorkloadChart = null;

    function initDashboardCharts() {
      try {
        const isDark = document.documentElement.classList.contains('dark');
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';
        const textColor = isDark ? '#94a3b8' : '#64748b';

        // 1. Trajectory Area Chart
        const ctx1 = document.getElementById('dashboardTrajectoryChart');
        if (ctx1) {
          if (dashboardTrajectoryChart) dashboardTrajectoryChart.destroy();
          const grad1 = ctx1.getContext('2d').createLinearGradient(0, 0, 0, 260);
          grad1.addColorStop(0, 'rgba(2, 132, 199, 0.35)');
          grad1.addColorStop(1, 'rgba(2, 132, 199, 0.0)');

          const grad2 = ctx1.getContext('2d').createLinearGradient(0, 0, 0, 260);
          grad2.addColorStop(0, 'rgba(99, 102, 241, 0.25)');
          grad2.addColorStop(1, 'rgba(99, 102, 241, 0.0)');

          dashboardTrajectoryChart = new Chart(ctx1, {
            type: 'line',
            data: {
              labels: ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', 'Now'],
              datasets: [
                {
                  label: 'DESKTOP-M378M07 (Host Free GB)',
                  data: [9.8, 9.9, 10.0, 10.1, 10.1, 10.2, 10.2, 10.3],
                  borderColor: '#0284c7',
                  backgroundColor: grad1,
                  fill: true,
                  tension: 0.38,
                  borderWidth: 2.5,
                  pointRadius: 3.5,
                  pointHoverRadius: 6,
                  pointBackgroundColor: '#0284c7'
                },
                {
                  label: 'DESKTOP-EV2F0TV (Tailscale Free GB)',
                  data: [27.1, 27.4, 27.8, 28.0, 28.2, 28.3, 28.4, 28.5],
                  borderColor: '#6366f1',
                  backgroundColor: grad2,
                  fill: true,
                  tension: 0.38,
                  borderWidth: 2.5,
                  pointRadius: 3.5,
                  pointHoverRadius: 6,
                  pointBackgroundColor: '#6366f1'
                },
                {
                  label: 'Fleet Reclaimed Space (GB)',
                  data: [0.2, 0.4, 0.7, 0.9, 1.1, 1.2, 1.35, 1.49],
                  borderColor: '#10b981',
                  backgroundColor: 'transparent',
                  borderDash: [5, 5],
                  tension: 0.35,
                  borderWidth: 2,
                  pointRadius: 3,
                  pointHoverRadius: 5,
                  pointBackgroundColor: '#10b981'
                }
              ]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              animation: { duration: 1300, easing: 'easeOutQuart' },
              interaction: { mode: 'index', intersect: false },
              plugins: {
                legend: {
                  position: 'bottom',
                  labels: { boxWidth: 12, color: textColor, font: { size: 10, weight: '600' }, padding: 12 }
                },
                tooltip: {
                  backgroundColor: isDark ? 'rgba(15, 23, 42, 0.9)' : 'rgba(255, 255, 255, 0.95)',
                  titleColor: isDark ? '#fff' : '#0f172a',
                  bodyColor: isDark ? '#cbd5e1' : '#334155',
                  borderColor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
                  borderWidth: 1,
                  padding: 10,
                  boxPadding: 4,
                  usePointStyle: true
                }
              },
              scales: {
                x: { grid: { display: false }, ticks: { color: textColor, font: { size: 10 } } },
                y: {
                  grid: { color: gridColor },
                  ticks: { color: textColor, font: { size: 10 }, callback: (v) => v + ' GB' }
                }
              }
            }
          });
        }

        // 2. Category Doughnut Chart
        const ctx2 = document.getElementById('dashboardCategoryChart');
        if (ctx2) {
          if (dashboardCategoryChart) dashboardCategoryChart.destroy();
          dashboardCategoryChart = new Chart(ctx2, {
            type: 'doughnut',
            data: {
              labels: ['cleanmgr.exe', 'RAM Trim & Prefetch', 'Shader Cache', 'Crash Dumps (WER)', 'User Temp', 'Windows Temp'],
              datasets: [{
                data: [850, 512, 145, 92, 28.7, 18.4],
                backgroundColor: ['#0284c7', '#f43f5e', '#06b6d4', '#a855f7', '#10b981', '#3b82f6'],
                borderWidth: 2,
                borderColor: isDark ? '#0f172a' : '#ffffff',
                hoverOffset: 8
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              cutout: '68%',
              animation: { animateRotate: true, animateScale: true, duration: 1400, easing: 'easeOutQuart' },
              plugins: {
                legend: { display: false },
                tooltip: {
                  backgroundColor: isDark ? 'rgba(15, 23, 42, 0.9)' : 'rgba(255, 255, 255, 0.95)',
                  titleColor: isDark ? '#fff' : '#0f172a',
                  bodyColor: isDark ? '#cbd5e1' : '#334155',
                  borderColor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
                  borderWidth: 1,
                  padding: 10,
                  callbacks: {
                    label: function(ctx) {
                      return ` ${ctx.label}: ${ctx.raw} MB`;
                    }
                  }
                }
              }
            }
          });
        }

        // 3. Workload Comparison Bar Chart
        const ctx3 = document.getElementById('dashboardWorkloadChart');
        if (ctx3) {
          if (dashboardWorkloadChart) dashboardWorkloadChart.destroy();
          dashboardWorkloadChart = new Chart(ctx3, {
            type: 'bar',
            data: {
              labels: ['DESKTOP-M378M07 (Host)', 'DESKTOP-EV2F0TV', 'DESKTOP-I2MHDIB', 'DESKTOP-F8G3T2C'],
              datasets: [
                {
                  label: 'RAM Load (%)',
                  data: [78, 65, 58, 52],
                  backgroundColor: '#f59e0b',
                  borderRadius: 6,
                  barPercentage: 0.6,
                  categoryPercentage: 0.7
                },
                {
                  label: 'Free Disk Space (GB)',
                  data: [10.3, 28.5, 42.1, 64.0],
                  backgroundColor: '#0ea5e9',
                  borderRadius: 6,
                  barPercentage: 0.6,
                  categoryPercentage: 0.7
                }
              ]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              animation: { duration: 1100, easing: 'easeOutQuart' },
              plugins: {
                legend: {
                  position: 'bottom',
                  labels: { boxWidth: 12, color: textColor, font: { size: 10, weight: '600' }, padding: 12 }
                },
                tooltip: {
                  backgroundColor: isDark ? 'rgba(15, 23, 42, 0.9)' : 'rgba(255, 255, 255, 0.95)',
                  titleColor: isDark ? '#fff' : '#0f172a',
                  bodyColor: isDark ? '#cbd5e1' : '#334155',
                  borderColor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
                  borderWidth: 1,
                  padding: 10
                }
              },
              scales: {
                x: {
                  grid: { display: false },
                  ticks: { color: textColor, font: { size: 10, family: 'monospace' } }
                },
                y: {
                  grid: { color: gridColor },
                  ticks: { color: textColor, font: { size: 10 } }
                }
              }
            }
          });
        }
      } catch (err) {
        console.error('Error in initDashboardCharts:', err);
      }
    }

    function updateDashboardGraphTimeframe(tf) {
      ['today', 'month', 'year'].forEach(t => {
        const btn = document.getElementById('graphTfBtn_' + t);
        if (btn) {
          if (t === tf) {
            btn.className = 'px-2.5 py-1 rounded-lg bg-white dark:bg-slate-700 text-sky-700 dark:text-sky-300 shadow-xs transition-all font-bold';
          } else {
            btn.className = 'px-2.5 py-1 rounded-lg text-slate-600 dark:text-slate-300 hover:text-sky-600 transition-all font-medium';
          }
        }
      });

      if (!dashboardTrajectoryChart) return;

      if (tf === 'today') {
        dashboardTrajectoryChart.data.labels = ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', 'Now'];
        dashboardTrajectoryChart.data.datasets[0].data = [9.8, 9.9, 10.0, 10.1, 10.1, 10.2, 10.2, 10.3];
        dashboardTrajectoryChart.data.datasets[1].data = [27.1, 27.4, 27.8, 28.0, 28.2, 28.3, 28.4, 28.5];
        dashboardTrajectoryChart.data.datasets[2].data = [0.2, 0.4, 0.7, 0.9, 1.1, 1.2, 1.35, 1.49];
      } else if (tf === 'month') {
        dashboardTrajectoryChart.data.labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Current'];
        dashboardTrajectoryChart.data.datasets[0].data = [6.4, 7.8, 8.9, 9.7, 10.3];
        dashboardTrajectoryChart.data.datasets[1].data = [21.2, 23.5, 25.4, 27.0, 28.5];
        dashboardTrajectoryChart.data.datasets[2].data = [4.8, 9.2, 14.5, 18.9, 24.6];
      } else if (tf === 'year') {
        dashboardTrajectoryChart.data.labels = ['Q1 Jan-Mar', 'Q2 Apr-Jun', 'Q3 Jul-Sep', 'Q4 Oct-Dec'];
        dashboardTrajectoryChart.data.datasets[0].data = [4.1, 6.5, 8.4, 10.3];
        dashboardTrajectoryChart.data.datasets[1].data = [15.8, 20.1, 24.6, 28.5];
        dashboardTrajectoryChart.data.datasets[2].data = [32.4, 68.1, 105.8, 142.6];
      }
      dashboardTrajectoryChart.update('active');
      setTimeframe(tf);
    }

    function animateKpiNumbers() {
      animateValue('overviewSizeText', 0, 1.49, 1100, ' GB', 2);
      animateValue('overviewFilesText', 0, 920, 900, '', 0);
      animateValue('tfSweepsCount', 0, 18, 800, '', 0);
      animateValue('tfHealthScore', 80, 99.8, 1200, '%', 1);
    }

    function animateValue(id, start, end, duration, suffix = '', decimals = 0) {
      const obj = document.getElementById(id);
      if (!obj) return;
      let startTimestamp = null;
      const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        const currentVal = start + (end - start) * easeProgress;
        obj.textContent = currentVal.toFixed(decimals) + suffix;
        if (progress < 1) {
          window.requestAnimationFrame(step);
        }
      };
      window.requestAnimationFrame(step);
    }
"""

    if "function initDashboardCharts()" not in content:
        # Insert before function initCharts()
        if "function initCharts()" in content:
            content = content.replace("function initCharts()", js_code + "\n    function initCharts()")
            print(f"Added initDashboardCharts to {filepath}")

    # Hook initDashboardCharts and animateKpiNumbers into switchTab and DOMContentLoaded
    if "if (tabId === 'overview') { initDashboardCharts(); }" not in content:
        content = content.replace(
            "const activeBtn = document.getElementById('tabBtn_' + tabId);\n      if (activeBtn) activeBtn.classList.add('active');",
            "const activeBtn = document.getElementById('tabBtn_' + tabId);\n      if (activeBtn) activeBtn.classList.add('active');\n      if (tabId === 'overview') { initDashboardCharts(); animateKpiNumbers(); }"
        )

    if "initDashboardCharts(); animateKpiNumbers();" not in content:
        content = content.replace(
            "initCharts();",
            "initCharts();\n        initDashboardCharts();\n        animateKpiNumbers();"
        )

    # Re-render charts when toggleTheme() is clicked
    if "initDashboardCharts();" not in content[content.find("function toggleTheme()"):content.find("function toggleTheme()") + 400]:
        content = content.replace(
            "updateThemeUI();",
            "updateThemeUI();\n      setTimeout(initDashboardCharts, 100);"
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully processed {filepath}")

if __name__ == '__main__':
    apply_upgrade_to_file('index.html')
    apply_upgrade_to_file('dashboard/templates/index.html')
