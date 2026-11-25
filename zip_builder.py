"""
NUNES AUTONOMOUS FLEET - REAL-TIME ZIP REGENERATOR
=================================================
Ensures that NUNES_FLEET_CLIENT_V7.zip and NUNES_CACHE_CLEANER_4H_AUTOMATION.zip
are dynamically kept 100% up-to-date with the latest scripts, batches,
and configuration files.
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent

CLIENT_FILES = [
    'START_AUTO_CLEANER.bat',
    'CONNECT_THIS_PC.bat',
    'CONNECT_FLEET_PC.bat',
    'TURN_DRIVE_BLUE_ELEVATED.bat',
    'prompt_backup_manager.py',
    'nunes_fleet_agent.ps1',
    'nunes_universal_cleaner.py',
    'hang_resolver.py',
    'cleaner.py',
    'NUNES_CACHE_CLEANER.bat',
    'AUTONOMOUS_CACHE_CLEANER.bat',
    'INSTALL_4H_SERVICE.bat',
    'UNINSTALL_SERVICE.bat',
    'RESOLVE_HANG_EMERGENCY.bat',
    'STATUS.bat',
    'SHOW_DETAILS.bat',
    'show_status.ps1',
    'install_linux.sh',
    'install_mac.sh',
    'README_SETUP.txt'
]

PRIMARY_ZIP_NAME = 'NUNES_FLEET_CLIENT_V7.zip'
SECONDARY_ZIP_NAME = 'NUNES_CACHE_CLEANER_4H_AUTOMATION.zip'

def get_latest_source_mtime():
    """Returns the maximum modification time among all client source files."""
    latest = 0
    for rel_path in CLIENT_FILES:
        fp = ROOT_DIR / rel_path
        if fp.exists():
            try:
                mtime = fp.stat().st_mtime
                if mtime > latest:
                    latest = mtime
            except Exception:
                pass
    return latest

def needs_rebuild(zip_path: Path) -> bool:
    """Returns True if the zip file doesn't exist or is older than any source file."""
    if not zip_path.exists():
        return True
    try:
        zip_mtime = zip_path.stat().st_mtime
        source_mtime = get_latest_source_mtime()
        return source_mtime > zip_mtime
    except Exception:
        return True

def build_client_zip(target_path: Path = None, verbose: bool = True) -> Path:
    """Rebuilds the client zip package with the latest source files."""
    if target_path is None:
        target_path = ROOT_DIR / PRIMARY_ZIP_NAME
    
    temp_zip = target_path.with_suffix('.tmp')
    files_added = 0
    total_uncompressed = 0

    with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel_name in CLIENT_FILES:
            src_file = ROOT_DIR / rel_name
            if src_file.exists():
                zf.write(src_file, arcname=rel_name)
                files_added += 1
                total_uncompressed += src_file.stat().st_size

    # Atomically replace target
    if target_path.exists():
        target_path.unlink()
    temp_zip.replace(target_path)

    # Also mirror to secondary zip
    secondary = ROOT_DIR / SECONDARY_ZIP_NAME
    if target_path != secondary:
        shutil.copy2(target_path, secondary)

    compressed_size = target_path.stat().st_size
    ratio = (1 - (compressed_size / total_uncompressed)) * 100 if total_uncompressed else 0

    if verbose:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [OK] Rebuilt {target_path.name}: {files_added} files, "
              f"{compressed_size:,} bytes (saved {ratio:.1f}%).")
    
    return target_path

def ensure_fresh_zip(force: bool = False, verbose: bool = False) -> Path:
    """
    Checks if any source file is newer than the zip.
    If so (or if force=True), rebuilds immediately and returns Path to fresh zip.
    """
    primary = ROOT_DIR / PRIMARY_ZIP_NAME
    if force or needs_rebuild(primary):
        return build_client_zip(primary, verbose=verbose)
    return primary

if __name__ == '__main__':
    print("[*] Checking NUNES Client ZIP status...")
    zip_path = ensure_fresh_zip(force=True, verbose=True)
    print(f"[OK] Up-to-date zip ready at: {zip_path}")
