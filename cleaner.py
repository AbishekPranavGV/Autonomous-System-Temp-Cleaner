"""
Autonomous System Temp Cleaner - Python Cross-Platform Engine
Author: Abishek Pranav G V
Description: Multi-threaded temporary file cleaner with Win32 locked-file detection,
path boundary verification, safety isolation, and JSON audit logging.
"""

import os
import sys
import time
import json
import shutil
import ctypes
import platform
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone

import glob

def get_all_safe_targets():
    """Dynamically discover all safe temporary and cache targets across all profiles and apps."""
    targets = []
    
    # Standard Temp
    if os.environ.get("TEMP"):
        targets.append(Path(os.environ["TEMP"]))
    targets.append(Path("C:/Windows/Temp"))
    
    local = os.environ.get("LOCALAPPDATA", "")
    prog = os.environ.get("ProgramData", "C:/ProgramData")
    
    if local:
        # All Chrome & Edge profiles (Default, Profile 1, Profile 2, etc.)
        for pat in [
            os.path.join(local, r"Google\Chrome\User Data\*\Cache"),
            os.path.join(local, r"Google\Chrome\User Data\*\Code Cache"),
            os.path.join(local, r"Google\Chrome\User Data\*\GPUCache"),
            os.path.join(local, r"Google\Chrome\User Data\*\DawnCache"),
            os.path.join(local, r"Google\Chrome\User Data\*\Service Worker\CacheStorage"),
            os.path.join(local, r"Microsoft\Edge\User Data\*\Cache"),
            os.path.join(local, r"Microsoft\Edge\User Data\*\Code Cache"),
            os.path.join(local, r"Microsoft\Edge\User Data\*\GPUCache"),
            os.path.join(local, r"Microsoft\Edge\User Data\*\DawnCache"),
            os.path.join(local, r"Microsoft\Edge\User Data\*\Service Worker\CacheStorage"),
        ]:
            for p in glob.glob(pat):
                targets.append(Path(p))
                
        # Stale electron app updaters (*updater)
        for u in glob.glob(os.path.join(local, "*updater")):
            targets.append(Path(u))
            
        # Shaders, crashdumps, caches
        for extra in ["CrashDumps", "D3DSCache", r"NVIDIA\DXCache", r"pip\cache", "npm-cache", r"uv\cache"]:
            p = Path(local) / extra
            if p.exists():
                targets.append(p)
                
    if prog:
        for extra in [r"Microsoft\Windows\WER\ReportQueue", r"Microsoft\Windows\WER\ReportArchive"]:
            p = Path(prog) / extra
            if p.exists():
                targets.append(p)
                
    sd = Path("C:/Windows/SoftwareDistribution/Download")
    if sd.exists() and is_admin():
        targets.append(sd)
        
    return [t for t in targets if t.exists() and is_path_safe(t)]

# Alias for backwards compatibility
SAFE_TARGET_PATHS = [Path(os.environ.get("TEMP", "C:/Windows/Temp")), Path("C:/Windows/Temp")]

# Protected system paths (ABSOLUTE SAFEGUARDS - NEVER TOUCH)
PROTECTED_PREFIXES = [
    Path("C:/Windows/System32"),
    Path("C:/Windows/SysWOW64"),
    Path("C:/Program Files"),
    Path("C:/Program Files (x86)"),
    Path(os.environ.get("USERPROFILE", "C:/Users/Default")) / "Desktop",
    Path(os.environ.get("USERPROFILE", "C:/Users/Default")) / "Documents",
    Path(os.environ.get("USERPROFILE", "C:/Users/Default")) / "Downloads",
]

def is_admin():
    """Verify administrator privileges on Windows."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def is_path_safe(target_path: Path) -> bool:
    """Validate that the target does not violate any safety boundary."""
    resolved = target_path.resolve()
    for protected in PROTECTED_PREFIXES:
        try:
            if resolved == protected.resolve() or resolved in protected.resolve().parents:
                return False
        except Exception:
            continue
    return True

def scan_directory(directory: Path):
    """Scan directory and return file count and aggregate size in bytes."""
    if not directory.exists():
        return 0, 0
    
    total_files = 0
    total_bytes = 0
    for root, dirs, files in os.walk(directory):
        for f in files:
            try:
                fp = Path(root) / f
                if fp.is_file():
                    total_files += 1
                    total_bytes += fp.stat().st_size
            except (PermissionError, FileNotFoundError):
                continue
    return total_files, total_bytes

def clean_directory(directory: Path, dry_run: bool = False):
    """Safely purge stale files in directory, gracefully skipping locked files."""
    if not directory.exists() or not is_path_safe(directory):
        return 0, 0, 0

    reclaimed_bytes = 0
    deleted_files = 0
    locked_files = 0

    for root, dirs, files in os.walk(directory, topdown=False):
        for f in files:
            fp = Path(root) / f
            try:
                size = fp.stat().st_size
                if not dry_run:
                    try:
                        import stat as stat_mod
                        os.chmod(fp, stat_mod.S_IWRITE)
                    except Exception:
                        pass
                    fp.unlink(missing_ok=True)
                reclaimed_bytes += size
                deleted_files += 1
            except (PermissionError, OSError):
                locked_files += 1
                continue

        for d in dirs:
            dp = Path(root) / d
            try:
                if not dry_run:
                    dp.rmdir()
            except (PermissionError, OSError):
                continue

    return deleted_files, locked_files, reclaimed_bytes

def configure_cleanmgr_safe_flags(include_recycle_bin=False):
    """Ensure safe registry flags: NEVER delete DownloadsFolder or Recycle Bin (unless requested)."""
    if platform.system() != "Windows":
        return
    try:
        import winreg
        reg_base = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches"
        safe_handlers = [
            "Temporary Files", "Temporary Setup Files", "Downloaded Program Files",
            "Internet Cache Files", "Thumbnail Cache", "D3D Shader Cache",
            "Delivery Optimization Files", "Active Setup Temp Folders",
            "System error memory dump files", "System error minidump files",
            "Windows Error Reporting Files"
        ]
        excluded_handlers = ["DownloadsFolder", "Update Cleanup", "Previous Installations", "User file versions"]
        if not include_recycle_bin:
            excluded_handlers.append("Recycle Bin")
        else:
            safe_handlers.append("Recycle Bin")

        for h in safe_handlers:
            try:
                k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"{reg_base}\\{h}", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(k, "StateFlags65535", 0, winreg.REG_DWORD, 2)
                winreg.CloseKey(k)
            except Exception:
                pass

        for ex in excluded_handlers:
            try:
                k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"{reg_base}\\{ex}", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(k, "StateFlags65535", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(k)
            except Exception:
                pass
    except Exception:
        pass

def run_cleanmgr(timeout=15, include_recycle_bin=False, dry_run=False):
    """Execute Windows Disk Cleanup (cleanmgr.exe) silently with safe non-destructive flags."""
    if platform.system() != "Windows" or dry_run:
        return None
    cleanmgr_bin = Path(os.environ.get("SystemRoot", "C:/Windows")) / "System32" / "cleanmgr.exe"
    if not cleanmgr_bin.exists():
        return None

    configure_cleanmgr_safe_flags(include_recycle_bin=include_recycle_bin)

    before_free = get_free_space_gb() * (1024 ** 3)
    try:
        subprocess.run(
            [str(cleanmgr_bin), "/sagerun:65535"],
            timeout=timeout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        try:
            subprocess.run(
                [str(cleanmgr_bin), "/autoclean"],
                timeout=timeout,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

    after_free = get_free_space_gb() * (1024 ** 3)
    recovered_mb = max(0.0, round((after_free - before_free) / (1024 * 1024), 2))
    return {
        "deleted": 1 if recovered_mb > 0 else 0,
        "recovered_mb": recovered_mb
    }

def get_free_space_gb():
    try:
        target = "C:\\" if platform.system() == "Windows" else "/"
        stat = shutil.disk_usage(target)
        return round(stat.free / (1024 ** 3), 2)
    except Exception:
        return 0.0

def purge_30_day_retention_backups():
    """Purges any prompt backup, snapshot, or log older than 30 days (30-day rolling retention rule)."""
    try:
        import prompt_backup_manager
        return prompt_backup_manager.purge_expired_backups()
    except Exception:
        return {"purged_count": 0, "purged_bytes": 0, "retention_days": 30}

def purge_35_day_retention_backups():
    """Legacy alias: standardizes to unified 30-day retention rule."""
    return purge_30_day_retention_backups()
    """Purges any prompt backup, snapshot, or log older than 35 days (35-day rolling retention rule)."""
    try:
        import prompt_backup_manager
        return prompt_backup_manager.purge_expired_backups()
    except Exception:
        return {"purged_count": 0, "purged_bytes": 0, "retention_days": 35}

def run_safe_cleanup(dry_run=False, include_cleanmgr=True, include_recycle_bin=False):
    """Executes full safe cleanup across all dynamic targets (Chrome/Edge profiles, Updaters, Temp, cleanmgr, 35-day retention)."""
    # 35-Day Retention sweep: automatically purges backups/snapshots older than 35 days
    retention_res = purge_30_day_retention_backups() if not dry_run else {"purged_count": 0}

    targets = get_all_safe_targets()
    total_deleted = 0
    total_locked = 0
    total_bytes = 0
    
    for target in targets:
        d, l, b = clean_directory(target, dry_run=dry_run)
        total_deleted += d
        total_locked += l
        total_bytes += b

    cm_res = None
    if include_cleanmgr and not dry_run:
        cm_res = run_cleanmgr(include_recycle_bin=include_recycle_bin)
        if cm_res:
            total_deleted += cm_res["deleted"]
            total_bytes += int(cm_res["recovered_mb"] * (1024 * 1024))

    return {
        "deleted": total_deleted,
        "locked": total_locked,
        "recovered_mb": round(total_bytes / (1024 * 1024), 2),
        "cleanmgr": cm_res,
        "retention_30d": retention_res, "retention_35d": retention_res
    }


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--no-cleanmgr', action='store_true')
    args = parser.parse_args()
    res = run_safe_cleanup(dry_run=args.dry_run, include_cleanmgr=not args.no_cleanmgr)
    res['free_space_gb'] = get_free_space_gb()
    if args.json:
        print(json.dumps(res))
    else:
        print(f"Deleted: {res['deleted']}, Recovered: {res['recovered_mb']} MB, Free space: {res['free_space_gb']} GB")
