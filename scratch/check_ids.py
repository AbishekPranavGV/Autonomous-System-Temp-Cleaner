import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target_ids = [
    'btnScanSelected', 'btnCleanSelected', 'btnAntiHang',
    'adminBadge', 'scanStatusBadge', 'scanStatusText',
    'nextLoopClock', 'themeToggleBtn', 'themeIcon', 'themeText',
    'btnNavDashboard', 'btnNavLiveFiles', 'navLiveFilesCount'
]

for tid in target_ids:
    matches = re.findall(rf'document\.getElementById\([\'\"]{tid}[\'\"]\)', text)
    print(f'{tid}: found {len(matches)} getElementById calls')
