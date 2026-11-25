# -*- coding: utf-8 -*-
import sys
import urllib.request
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

live_url = "https://autonomous-system-temp-cleaner-six.vercel.app"
print(f"Verifying live site: {live_url}")

req = urllib.request.Request(live_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        status = resp.status
        html = resp.read().decode('utf-8')
        print(f"Live HTTP Status: {status}")
        print(f"Content Length: {len(html)} bytes")
        
        # 1. Check Sidebar
        has_sidebar = 'id="appSidebar"' in html
        print(f"Sidebar present: {has_sidebar}")
        
        # 2. Check Global Search
        has_search = 'id="globalFleetSearch"' in html
        print(f"Global search present: {has_search}")
        
        # 3. Check Notification Center
        has_notif = 'id="notificationCenterContainer"' in html
        print(f"Notification Center present: {has_notif}")
        
        # 4. Check 4-Step Cleanup Modal
        has_workflow = 'id="cleanupWorkflowModal"' in html
        print(f"4-step cleanup workflow modal present: {has_workflow}")
        
        # 5. Check Node Inspector Drawer
        has_drawer = 'id="nodeDetailDrawer"' in html
        print(f"Node detail inspector drawer present: {has_drawer}")
        
        # 6. Check Trajectory Chart
        has_chart = 'chartStorageTrajectory' in html
        has_nodes = all(n in html for n in ['DESKTOP-M378M07', 'DESKTOP-EV2F0TV', 'DESKTOP-I2MHDIB', 'DESKTOP-F8G3T2C'])
        print(f"Trajectory chart present: {has_chart}")
        print(f"All 4 fleet nodes in HTML: {has_nodes}")
        
        # 7. Check Department: texts
        has_dept = 'Department:' in html
        print(f"Stray 'Department:' text present: {has_dept} (Expected: False)")
        
        # 8. Check stray quotes/ticks
        has_triple_quotes = "'''" in html
        print(f"Stray ''' present: {has_triple_quotes} (Expected: False)")
        
        # 9. Verify Tail
        ends_cleanly = html.strip().endswith('</html>')
        print(f"Ends cleanly with </html>: {ends_cleanly}")
        
except Exception as e:
    print(f"Verification error: {e}")
