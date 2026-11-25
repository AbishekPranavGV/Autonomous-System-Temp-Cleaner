import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

wer_dirs = [
    Path(os.environ.get('LOCALAPPDATA', '')) / 'CrashDumps',
    Path(os.environ.get('ProgramData', 'C:/ProgramData')) / 'Microsoft' / 'Windows' / 'WER' / 'ReportArchive'
]

for d in wer_dirs:
    if d.exists():
        files = list(d.glob('*'))
        print(f"Dir {d} exists, count: {len(files)}")
    else:
        print(f"Dir {d} does not exist")
