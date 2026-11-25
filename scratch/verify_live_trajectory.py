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
    idx = html.rfind('</html>')
    after = html[idx+7:]
    print("Content after </html>:", repr(after))
    print("Has ''' in HTML:", "'''" in html)
    print("Has DESKTOP-M378M07 in trajectory:", "DESKTOP-M378M07 (Host)" in html)
    print("Has DESKTOP-EV2F0TV in trajectory:", "DESKTOP-EV2F0TV" in html)
    print("Has DESKTOP-I2MHDIB in trajectory:", "DESKTOP-I2MHDIB" in html)
    print("Has DESKTOP-F8G3T2C in trajectory:", "DESKTOP-F8G3T2C" in html)
    print("Has STORAGE CAPACITY TRAJECTORY (GB):", "STORAGE CAPACITY TRAJECTORY (GB)" in html)
    print("Has Past 24 Hours label:", "Past 24 Hours" in html)
except Exception as e:
    print("Error fetching URL:", e)
