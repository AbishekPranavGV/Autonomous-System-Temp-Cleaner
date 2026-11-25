# -*- coding: utf-8 -*-
import sys
import urllib.request

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

base = "https://autonomous-system-temp-cleaner-six.vercel.app"

assets = [
    '/favicon.svg',
    '/favicon.ico',
    '/favicon-32x32.png',
    '/favicon-16x16.png',
    '/apple-touch-icon.png',
    '/site.webmanifest'
]

print("Verifying browser tab icons & favicons on live site...")
for a in assets:
    url = f"{base}{a}"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            ct = r.headers.get('Content-Type')
            cl = len(r.read())
            print(f" [200 OK] {a} -> {ct} ({cl:,} bytes)")
    except Exception as e:
        print(f" [FAIL] {a} -> {e}")

# Check HTML head
print("\nChecking <head> favicon declarations...")
try:
    with urllib.request.urlopen(base, timeout=10) as r:
        html = r.read().decode('utf-8')
        has_svg = 'rel="icon" type="image/svg+xml"' in html
        has_ico = 'rel="alternate icon" href="/favicon.ico"' in html
        has_apple = 'rel="apple-touch-icon"' in html
        has_manifest = 'rel="manifest" href="/site.webmanifest"' in html
        print(f" SVG icon linked: {has_svg}")
        print(f" ICO icon linked: {has_ico}")
        print(f" Apple icon linked: {has_apple}")
        print(f" Webmanifest linked: {has_manifest}")
except Exception as e:
    print("HTML error:", e)
