import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

payload = json.dumps({'message': 'கணினி ஏன் மெதுவாக உள்ளது?', 'node': 'DESKTOP-M378M07', 'lang': 'ta'}).encode('utf-8')
req = urllib.request.Request('https://autonomous-system-temp-cleaner-six.vercel.app/api/ai/chat', data=payload, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req, timeout=10) as res:
    data = json.loads(res.read().decode('utf-8'))
    print('Live AI Chat status:', data.get('success'))
    print('Risk:', data.get('data', {}).get('risk'))
    print('Reply preview:\n', data.get('data', {}).get('reply')[:250])
