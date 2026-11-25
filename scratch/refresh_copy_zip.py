import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
copy_zip = root_dir / 'Autonomous-System-Temp-Cleaner-COPY.zip'

if copy_zip.exists():
    print("Found existing COPY zip, updating key files...")
    # Update index.html and nunes_fleet_agent.ps1 in the copy zip
    with zipfile.ZipFile(copy_zip, 'a', zipfile.ZIP_DEFLATED) as zf:
        zf.write(root_dir / 'index.html', arcname='index.html')
        zf.write(root_dir / 'cleaner.py', arcname='cleaner.py')
        zf.write(root_dir / 'prompt_backup_manager.py', arcname='prompt_backup_manager.py')
        zf.write(root_dir / 'nunes_fleet_agent.ps1', arcname='nunes_fleet_agent.ps1')
    print("Autonomous-System-Temp-Cleaner-COPY.zip refreshed successfully!")
