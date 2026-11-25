with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Total lines in index.html:", len(lines))
# Find main landmarks
for i, l in enumerate(lines):
    if any(k in l for k in ['<header', '<nav', '<main', '<dialog', 'id="sec_overview"', 'id="sec_settings"', '<!-- Modals -->', '<!-- AI Chatbot Drawer -->']):
        print(f"Line {i+1}: {l.strip()[:100]}")
