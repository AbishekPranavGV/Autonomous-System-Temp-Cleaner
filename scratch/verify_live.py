import urllib.request
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request(
    'https://autonomous-system-temp-cleaner-six.vercel.app',
    headers={'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')

    print("HTTP Status: 200 OK")
    print('"btnHeaderDashboard" in live HTML:', 'btnHeaderDashboard' in html)
    print('"dashboardGraphsSuite" in live HTML:', 'dashboardGraphsSuite' in html)
    print('"dashboardTrajectoryChart" in live HTML:', 'dashboardTrajectoryChart' in html)
    print('"dashboardCategoryChart" in live HTML:', 'dashboardCategoryChart' in html)
    print('"dashboardWorkloadChart" in live HTML:', 'dashboardWorkloadChart' in html)
    print('"initDashboardCharts" in live HTML:', 'initDashboardCharts' in html)
    print('"animateKpiNumbers" in live HTML:', 'animateKpiNumbers' in html)
    print('"1. Dashboard" in live HTML:', '1. Dashboard' in html)
    print('"Department:" in live HTML:', 'Department:' in html)
except Exception as e:
    print("Error fetching URL:", e)
