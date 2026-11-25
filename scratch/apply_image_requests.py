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

    # Part 1: Remove stray ''' after </html>
    if "</html>" in content:
        idx = content.rfind("</html>")
        content = content[:idx+7] + "\n"
        print(f"Cleaned trailing content after </html> in {filepath}")

    # Part 2: Update Section 1 graph HTML to match Image 2
    old_graph1_html = """            <div>
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
          </div>"""

    new_graph1_html = """            <div>
              <div class="flex items-center gap-2">
                <span class="relative flex h-2.5 w-2.5">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-sky-500"></span>
                </span>
                <h3 class="text-xs font-extrabold uppercase tracking-wider text-slate-900 dark:text-white" data-i18n="chart_trajectory_title">STORAGE CAPACITY TRAJECTORY (GB)</h3>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-sky-100 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300">4 WORKSTATIONS</span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5" data-i18n="chart_trajectory_sub">Detailed multi-node storage capacity trajectory across all connected office computers</p>
            </div>
            
            <!-- Graph Timeframe Switcher -->
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-mono text-slate-400 font-bold uppercase hidden sm:inline" id="trajectoryPeriodLabel">Past 24 Hours</span>
              <div class="flex items-center gap-1 p-1 bg-slate-100 dark:bg-slate-800 rounded-xl text-xs font-semibold">
                <button onclick="updateDashboardGraphTimeframe('today')" id="graphTfBtn_today" class="px-2.5 py-1 rounded-lg bg-white dark:bg-slate-700 text-sky-700 dark:text-sky-300 shadow-xs transition-all font-bold">Today</button>
                <button onclick="updateDashboardGraphTimeframe('month')" id="graphTfBtn_month" class="px-2.5 py-1 rounded-lg text-slate-600 dark:text-slate-300 hover:text-sky-600 transition-all font-medium">Month</button>
                <button onclick="updateDashboardGraphTimeframe('year')" id="graphTfBtn_year" class="px-2.5 py-1 rounded-lg text-slate-600 dark:text-slate-300 hover:text-sky-600 transition-all font-medium">Year</button>
              </div>
            </div>
          </div>

          <!-- Chart.js Canvas -->
          <div class="relative h-64 sm:h-72 w-full">
            <canvas id="dashboardTrajectoryChart"></canvas>
          </div>

          <!-- Micro Telemetry Bar under graph showing all 4 workstations -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-slate-100 dark:border-white/5 text-[11px] font-mono">
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-sky-500"></span> <span class="text-slate-500 dark:text-slate-400">DESKTOP-M378M07:</span> <strong class="text-slate-800 dark:text-slate-200">10.3 GB</strong></div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span> <span class="text-slate-500 dark:text-slate-400">DESKTOP-EV2F0TV:</span> <strong class="text-slate-800 dark:text-slate-200">28.5 GB</strong></div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-teal-500"></span> <span class="text-slate-500 dark:text-slate-400">DESKTOP-I2MHDIB:</span> <strong class="text-slate-800 dark:text-slate-200">42.1 GB</strong></div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> <span class="text-slate-500 dark:text-slate-400">DESKTOP-F8G3T2C:</span> <strong class="text-slate-800 dark:text-slate-200">64.0 GB</strong></div>
          </div>"""

    if old_graph1_html in content:
        content = content.replace(old_graph1_html, new_graph1_html)
        print(f"Updated Section 1 trajectory graph container in {filepath}")

    # Part 3: Update JavaScript for initDashboardCharts() to plot ALL 4 connected workstations
    old_init_dash = """        // 1. Trajectory Area Chart
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
        }"""

    new_init_dash = """        // 1. Trajectory Area Chart (Shows ALL 4 connected workstations)
        const ctx1 = document.getElementById('dashboardTrajectoryChart');
        if (ctx1) {
          if (dashboardTrajectoryChart) dashboardTrajectoryChart.destroy();
          const grad1 = ctx1.getContext('2d').createLinearGradient(0, 0, 0, 260);
          grad1.addColorStop(0, 'rgba(2, 132, 199, 0.22)');
          grad1.addColorStop(1, 'rgba(2, 132, 199, 0.0)');

          dashboardTrajectoryChart = new Chart(ctx1, {
            type: 'line',
            data: {
              labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', 'Now'],
              datasets: [
                {
                  label: 'DESKTOP-M378M07 (Host)',
                  data: [9.8, 9.9, 10.1, 10.1, 10.2, 10.2, 10.3],
                  borderColor: '#0284c7',
                  backgroundColor: grad1,
                  fill: true,
                  tension: 0.32,
                  borderWidth: 2.5,
                  pointRadius: 4,
                  pointHoverRadius: 7,
                  pointBackgroundColor: '#ffffff',
                  pointBorderColor: '#0284c7',
                  pointBorderWidth: 2
                },
                {
                  label: 'DESKTOP-EV2F0TV',
                  data: [27.2, 27.5, 27.9, 28.1, 28.3, 28.4, 28.5],
                  borderColor: '#6366f1',
                  backgroundColor: 'transparent',
                  tension: 0.32,
                  borderWidth: 2.5,
                  pointRadius: 4,
                  pointHoverRadius: 7,
                  pointBackgroundColor: '#ffffff',
                  pointBorderColor: '#6366f1',
                  pointBorderWidth: 2
                },
                {
                  label: 'DESKTOP-I2MHDIB',
                  data: [40.8, 41.2, 41.5, 41.8, 41.9, 42.0, 42.1],
                  borderColor: '#0d9488',
                  backgroundColor: 'transparent',
                  tension: 0.32,
                  borderWidth: 2.5,
                  pointRadius: 4,
                  pointHoverRadius: 7,
                  pointBackgroundColor: '#ffffff',
                  pointBorderColor: '#0d9488',
                  pointBorderWidth: 2
                },
                {
                  label: 'DESKTOP-F8G3T2C',
                  data: [62.5, 62.9, 63.2, 63.5, 63.7, 63.9, 64.0],
                  borderColor: '#d97706',
                  backgroundColor: 'transparent',
                  tension: 0.32,
                  borderWidth: 2.5,
                  pointRadius: 4,
                  pointHoverRadius: 7,
                  pointBackgroundColor: '#ffffff',
                  pointBorderColor: '#d97706',
                  pointBorderWidth: 2
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
                  labels: {
                    boxWidth: 12,
                    color: textColor,
                    font: { size: 11, weight: '600' },
                    padding: 16,
                    usePointStyle: true,
                    pointStyle: 'rectRounded'
                  }
                },
                tooltip: {
                  backgroundColor: isDark ? 'rgba(15, 23, 42, 0.95)' : 'rgba(255, 255, 255, 0.96)',
                  titleColor: isDark ? '#fff' : '#0f172a',
                  bodyColor: isDark ? '#cbd5e1' : '#334155',
                  borderColor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
                  borderWidth: 1,
                  padding: 10,
                  boxPadding: 4,
                  usePointStyle: true,
                  callbacks: {
                    label: function(context) {
                      return ` ${context.dataset.label}: ${context.raw} GB Free`;
                    }
                  }
                }
              },
              scales: {
                x: {
                  grid: { display: false },
                  ticks: { color: textColor, font: { size: 10, family: 'monospace' } }
                },
                y: {
                  min: 0,
                  max: 75,
                  grid: { color: gridColor },
                  ticks: {
                    stepSize: 15,
                    color: textColor,
                    font: { size: 10 },
                    callback: (v) => v + ' GB'
                  }
                }
              }
            }
          });
        }"""

    if old_init_dash in content:
        content = content.replace(old_init_dash, new_init_dash)
        print(f"Updated initDashboardCharts to all 4 nodes in {filepath}")

    # Part 4: Update updateDashboardGraphTimeframe to include all 4 connected nodes
    old_timeframe_code = """      if (tf === 'today') {
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
      }"""

    new_timeframe_code = """      const pLabel = document.getElementById('trajectoryPeriodLabel');
      if (tf === 'today') {
        if (pLabel) pLabel.textContent = 'Past 24 Hours';
        dashboardTrajectoryChart.data.labels = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', 'Now'];
        dashboardTrajectoryChart.data.datasets[0].data = [9.8, 9.9, 10.1, 10.1, 10.2, 10.2, 10.3];
        dashboardTrajectoryChart.data.datasets[1].data = [27.2, 27.5, 27.9, 28.1, 28.3, 28.4, 28.5];
        dashboardTrajectoryChart.data.datasets[2].data = [40.8, 41.2, 41.5, 41.8, 41.9, 42.0, 42.1];
        dashboardTrajectoryChart.data.datasets[3].data = [62.5, 62.9, 63.2, 63.5, 63.7, 63.9, 64.0];
      } else if (tf === 'month') {
        if (pLabel) pLabel.textContent = 'Past 30 Days';
        dashboardTrajectoryChart.data.labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Current'];
        dashboardTrajectoryChart.data.datasets[0].data = [6.4, 7.8, 8.9, 9.7, 10.3];
        dashboardTrajectoryChart.data.datasets[1].data = [21.2, 23.5, 25.4, 27.0, 28.5];
        dashboardTrajectoryChart.data.datasets[2].data = [34.1, 36.8, 38.9, 40.7, 42.1];
        dashboardTrajectoryChart.data.datasets[3].data = [55.2, 58.0, 60.4, 62.3, 64.0];
      } else if (tf === 'year') {
        if (pLabel) pLabel.textContent = 'Past 12 Months';
        dashboardTrajectoryChart.data.labels = ['Q1 Jan-Mar', 'Q2 Apr-Jun', 'Q3 Jul-Sep', 'Q4 Oct-Dec'];
        dashboardTrajectoryChart.data.datasets[0].data = [4.1, 6.5, 8.4, 10.3];
        dashboardTrajectoryChart.data.datasets[1].data = [15.8, 20.1, 24.6, 28.5];
        dashboardTrajectoryChart.data.datasets[2].data = [28.0, 32.5, 37.8, 42.1];
        dashboardTrajectoryChart.data.datasets[3].data = [46.5, 52.0, 58.2, 64.0];
      }"""

    if old_timeframe_code in content:
        content = content.replace(old_timeframe_code, new_timeframe_code)
        print(f"Updated timeframe switcher datasets in {filepath}")

    # Part 5: Update Section 6 initCharts() for chartStorageTrajectory to show all 4 connected nodes
    old_init_health = """        const ctx1 = document.getElementById('chartStorageTrajectory');
        if (ctx1) {
          new Chart(ctx1, {
            type: 'line',
            data: {
              labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', 'Now'],
              datasets: [
                {
                  label: 'DESKTOP-M378M07 (Host)',
                  data: [9.8, 9.9, 10.1, 10.1, 10.2, 10.2, 10.3],
                  borderColor: '#0284c7',
                  backgroundColor: 'rgba(2, 132, 199, 0.1)',
                  fill: true,
                  tension: 0.3
                },
                {
                  label: 'DESKTOP-EV2F0TV (Accounts)',
                  data: [27.2, 27.5, 27.9, 28.1, 28.3, 28.4, 28.5],
                  borderColor: '#6366f1',
                  backgroundColor: 'transparent',
                  tension: 0.3
                }
              ]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } } },
              scales: { y: { grid: { color: 'rgba(200, 200, 200, 0.1)' } }, x: { grid: { display: false } } }
            }
          });
        }"""

    new_init_health = """        const ctx1 = document.getElementById('chartStorageTrajectory');
        if (ctx1) {
          new Chart(ctx1, {
            type: 'line',
            data: {
              labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', 'Now'],
              datasets: [
                {
                  label: 'DESKTOP-M378M07 (Host)',
                  data: [9.8, 9.9, 10.1, 10.1, 10.2, 10.2, 10.3],
                  borderColor: '#0284c7',
                  backgroundColor: 'rgba(2, 132, 199, 0.1)',
                  fill: true,
                  tension: 0.3,
                  borderWidth: 2.5,
                  pointRadius: 4,
                  pointHoverRadius: 7,
                  pointBackgroundColor: '#ffffff',
                  pointBorderColor: '#0284c7',
                  pointBorderWidth: 2
                },
                {
                  label: 'DESKTOP-EV2F0TV',
                  data: [27.2, 27.5, 27.9, 28.1, 28.3, 28.4, 28.5],
                  borderColor: '#6366f1',
                  backgroundColor: 'transparent',
                  tension: 0.3,
                  borderWidth: 2.5,
                  pointRadius: 4,
                  pointHoverRadius: 7,
                  pointBackgroundColor: '#ffffff',
                  pointBorderColor: '#6366f1',
                  pointBorderWidth: 2
                },
                {
                  label: 'DESKTOP-I2MHDIB',
                  data: [40.8, 41.2, 41.5, 41.8, 41.9, 42.0, 42.1],
                  borderColor: '#0d9488',
                  backgroundColor: 'transparent',
                  tension: 0.3,
                  borderWidth: 2.5,
                  pointRadius: 4,
                  pointHoverRadius: 7,
                  pointBackgroundColor: '#ffffff',
                  pointBorderColor: '#0d9488',
                  pointBorderWidth: 2
                },
                {
                  label: 'DESKTOP-F8G3T2C',
                  data: [62.5, 62.9, 63.2, 63.5, 63.7, 63.9, 64.0],
                  borderColor: '#d97706',
                  backgroundColor: 'transparent',
                  tension: 0.3,
                  borderWidth: 2.5,
                  pointRadius: 4,
                  pointHoverRadius: 7,
                  pointBackgroundColor: '#ffffff',
                  pointBorderColor: '#d97706',
                  pointBorderWidth: 2
                }
              ]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: 'bottom',
                  labels: {
                    boxWidth: 12,
                    font: { size: 10, weight: '600' },
                    usePointStyle: true,
                    padding: 12
                  }
                }
              },
              scales: {
                y: {
                  min: 0,
                  max: 75,
                  grid: { color: 'rgba(200, 200, 200, 0.1)' },
                  ticks: { stepSize: 15, callback: (v) => v + ' GB' }
                },
                x: { grid: { display: false } }
              }
            }
          });
        }"""

    if old_init_health in content:
        content = content.replace(old_init_health, new_init_health)
        print(f"Updated Section 6 chartStorageTrajectory to all 4 nodes in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully processed {filepath}")

if __name__ == '__main__':
    update_file('index.html')
    update_file('dashboard/templates/index.html')
