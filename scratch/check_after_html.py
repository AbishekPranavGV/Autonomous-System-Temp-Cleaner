import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's check after </html>
idx = text.rfind('</html>')
if idx != -1:
    after = text[idx+7:]
    print("Content after </html>:")
    print(repr(after))
