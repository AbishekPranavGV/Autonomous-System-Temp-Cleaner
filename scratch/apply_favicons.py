# -*- coding: utf-8 -*-
import sys
import os
import urllib.parse
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('favicon.svg', 'r', encoding='utf-8') as f:
    svg_raw = f.read()

# Create clean URL-encoded data URI
# Replace newlines and multi-spaces
compact_svg = " ".join(svg_raw.split())
encoded_svg = urllib.parse.quote(compact_svg)
data_uri = f"data:image/svg+xml,{encoded_svg}"

FAVICON_TAGS = f"""  <!-- 🌟 Enterprise Favicons & High-Resolution Browser Tab Icons -->
  <link rel="icon" type="image/svg+xml" href="{data_uri}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="alternate icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#0284c7" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0b1120" media="(prefers-color-scheme: dark)">
  <meta name="apple-mobile-web-app-title" content="NUNES Fleet">
  <meta name="application-name" content="NUNES AI PC Command Center">
  <meta name="msapplication-TileColor" content="#0284c7">"""

print(f"Generated data URI (length: {len(data_uri)})")
print("Tags snippet:\n", FAVICON_TAGS[:300])

for fp in ['index.html', 'dashboard/templates/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean title
    import re
    content = re.sub(
        r'<title>.*?</title>',
        '<title>NUNES AI PC Command Center • v10.1 Enterprise | Windows Diagnostics & Fleet Sentry</title>',
        content
    )

    # Insert favicon tags if not present
    if 'rel="icon"' not in content:
        target = '<meta name="description"'
        if target in content:
            content = content.replace(target, FAVICON_TAGS + "\n  " + target)
            print(f"Inserted favicon tags into {fp}")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

# Patch dashboard/app.py to serve favicon routes
with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

if '@app.route(\'/favicon.ico\')' not in app_py:
    routes_code = """
@app.route('/favicon.ico')
@app.route('/favicon.svg')
@app.route('/favicon-32x32.png')
@app.route('/favicon-16x16.png')
@app.route('/apple-touch-icon.png')
@app.route('/site.webmanifest')
def serve_favicon():
    filename = request.path.lstrip('/')
    file_path = ROOT_DIR.parent / filename
    if file_path.exists():
        mime = 'image/x-icon' if filename.endswith('.ico') else ('image/svg+xml' if filename.endswith('.svg') else ('application/manifest+json' if filename.endswith('.webmanifest') else 'image/png'))
        return send_file(str(file_path), mimetype=mime)
    return ('', 404)
"""
    app_py = app_py.replace("@app.route('/api/version')", routes_code + "\n@app.route('/api/version')")
    with open('dashboard/app.py', 'w', encoding='utf-8') as f:
        f.write(app_py)
    print("Added favicon routes to dashboard/app.py")
