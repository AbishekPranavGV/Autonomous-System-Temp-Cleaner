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
        
        # 1. Check Body Tag
        has_correct_body = '<body class="h-screen w-screen overflow-hidden flex' in html
        print(f"Correct body flex container: {has_correct_body}")
        
        # 2. Check IST Clock
        has_ist_clock = 'LIVE • --:--:-- IST' in html or 'IST' in html
        has_kolkata_tz = 'Asia/Kolkata' in html
        print(f"IST Clock element present: {has_ist_clock}")
        print(f"Asia/Kolkata timezone in JS: {has_kolkata_tz}")
        
        # 3. Check Mobile Backdrop
        has_backdrop = 'id="mobileSidebarBackdrop"' in html
        print(f"Mobile backdrop present: {has_backdrop}")
        
        # 4. Check Mobile Hamburger
        has_hamburger = 'toggleMobileSidebar()' in html
        print(f"Mobile sidebar toggle present: {has_hamburger}")
        
        # 5. Check No stray quotes/ticks
        has_triple_quotes = "'''" in html
        print(f"Stray ''' present: {has_triple_quotes} (Expected: False)")
        
        # 6. Verify Tail
        ends_cleanly = html.strip().endswith('</html>')
        print(f"Ends cleanly with </html>: {ends_cleanly}")
        
except Exception as e:
    print(f"Verification error: {e}")
