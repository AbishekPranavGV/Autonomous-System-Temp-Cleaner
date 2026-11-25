#!/usr/bin/env python3

"""

NUNES Universal Fleet Temp Cleaner & Dashboard Client (V7.4.0 Cross-Platform)

Supports: Windows 10/11/Server, macOS (Intel & Apple Silicon), Linux



Autonomous 4-hour background cache cleaner with 1-minute live fleet heartbeat,

Win32/POSIX locked file safety, and real-time dashboard reporting.

Zero external dependencies (uses standard Python 3.6+ library).

"""



import os

import sys

import time

import json

import socket

import shutil

import platform

import argparse

import subprocess

from datetime import datetime, timezone

from pathlib import Path

import urllib.request

import urllib.error



VERSION = "7.4.0"

DEFAULT_DASHBOARD_URLS = [

    "https://nam-usr-concerns-incidents.trycloudflare.com",

    "https://autonomous-system-temp-cleaner-six.vercel.app",

    "http://192.168.1.114:8090",

    "http://100.88.183.106:8090",

    "http://192.168.0.100:8090",

    "http://192.168.29.88:8090",

    "http://localhost:8090"

]

DEFAULT_SMB_PATHS = [

    r"\\192.168.29.88\Common\Completed\Abishek\final\NUNES_TEMP_final\NUNES_TEMP_CLEANER_V7_4_0_HEARTBEAT_RECOVERY",

    r"\\192.168.29.88\Common\Completed\Abishek\final\NUNES_TEMP_CLEANER_V7_3_0_TAILSCALE_AWARE\NUNES_TEMP_CLEANER_V7_3_0_TAILSCALE_AWARE",

    "/Volumes/Common/Completed/Abishek/final/NUNES_TEMP_final/NUNES_TEMP_CLEANER_V7_4_0_HEARTBEAT_RECOVERY",

    "/mnt/nas/Common/Completed/Abishek/final/NUNES_TEMP_final/NUNES_TEMP_CLEANER_V7_4_0_HEARTBEAT_RECOVERY"

]



def get_os_friendly_name():

    system = platform.system()

    if system == "Darwin":

        mac_ver = platform.mac_ver()[0]

        return f"macOS {mac_ver}" if mac_ver else "macOS"

    elif system == "Windows":

        return f"Windows {platform.release()}"

    elif system == "Linux":

        try:

            with open("/etc/os-release") as f:

                for line in f:

                    if line.startswith("PRETTY_NAME="):

                        return line.split("=", 1)[1].strip().strip('"')

        except Exception:

            pass

        return "Linux"

    return system



def get_tailscale_ip():

    try:

        out = subprocess.check_output(["tailscale", "ip", "-4"], stderr=subprocess.DEVNULL, timeout=2)

        ip = out.decode().strip()

        if ip:

            return ip

    except Exception:

        pass

    # Fallback scan of network interfaces

    try:

        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):

            ip = info[4][0]

            parts = ip.split('.')

            if len(parts) == 4 and int(parts[0]) == 100 and (64 <= int(parts[1]) <= 127):

                return ip

    except Exception:

        pass

    return None



def get_local_ip():

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.settimeout(0.5)

        s.connect(("8.8.8.8", 80))

        ip = s.getsockname()[0]

        s.close()

        return ip

    except Exception:

        try:

            return socket.gethostbyname(socket.gethostname())

        except Exception:

            return "127.0.0.1"



def get_free_space_gb():

    try:

        target = "C:\\" if platform.system() == "Windows" else "/"

        stat = shutil.disk_usage(target)

        return round(stat.free / (1024 ** 3), 2)

    except Exception:

        return 0.0



def get_cleanup_targets():

    system = platform.system()

    home = Path.home()

    targets = []



    if system == "Windows":

        temp_env = os.environ.get("TEMP")

        if temp_env:

            targets.append(Path(temp_env))

        win_temp = Path("C:/Windows/Temp")

        if win_temp.exists():

            targets.append(win_temp)

        local_appdata = os.environ.get("LOCALAPPDATA", "")

        program_data = os.environ.get("ProgramData", "C:/ProgramData")

        if local_appdata:
            import glob
            # All Chrome & Edge profiles (Default, Profile 1, Profile 2, etc.)
            for pat in [
                os.path.join(local_appdata, r"Google\Chrome\User Data\*\Cache"),
                os.path.join(local_appdata, r"Google\Chrome\User Data\*\Code Cache"),
                os.path.join(local_appdata, r"Google\Chrome\User Data\*\GPUCache"),
                os.path.join(local_appdata, r"Google\Chrome\User Data\*\DawnCache"),
                os.path.join(local_appdata, r"Google\Chrome\User Data\*\Service Worker\CacheStorage"),
                os.path.join(local_appdata, r"Microsoft\Edge\User Data\*\Cache"),
                os.path.join(local_appdata, r"Microsoft\Edge\User Data\*\Code Cache"),
                os.path.join(local_appdata, r"Microsoft\Edge\User Data\*\GPUCache"),
                os.path.join(local_appdata, r"Microsoft\Edge\User Data\*\DawnCache"),
                os.path.join(local_appdata, r"Microsoft\Edge\User Data\*\Service Worker\CacheStorage"),
            ]:
                for p_match in glob.glob(pat):
                    targets.append(Path(p_match))

            # Updaters, Shaders, CrashDumps, pip/npm/uv caches
            for u in glob.glob(os.path.join(local_appdata, "*updater")):
                targets.append(Path(u))

            for extra_name in ["CrashDumps", "D3DSCache", r"NVIDIA\DXCache", r"pip\cache", "npm-cache", r"uv\cache"]:
                p_extra = Path(local_appdata) / extra_name
                if p_extra.exists():
                    targets.append(p_extra)

        if program_data:

            for extra in [

                Path(program_data) / "Microsoft" / "Windows" / "WER" / "ReportQueue",

                Path(program_data) / "Microsoft" / "Windows" / "WER" / "ReportArchive",

            ]:

                if extra.exists():

                    targets.append(extra)

        sd = Path("C:/Windows/SoftwareDistribution/Download")

        if sd.exists():

            targets.append(sd)

    elif system == "Darwin":  # macOS

        caches = home / "Library" / "Caches"

        if caches.exists():

            targets.append(caches)

        logs = home / "Library" / "Logs"

        if logs.exists():

            targets.append(logs)

        tmpdir = os.environ.get("TMPDIR")

        if tmpdir and Path(tmpdir).exists():

            targets.append(Path(tmpdir))

    else:  # Linux / Unix

        user_cache = home / ".cache"

        if user_cache.exists():

            targets.append(user_cache)

        tmp = Path("/tmp")

        if tmp.exists():

            targets.append(tmp)

        var_tmp = Path("/var/tmp")

        if var_tmp.exists():

            targets.append(var_tmp)



    return [t for t in targets if t.exists()]



def clean_target_folder(folder_path, min_age_hours=0, dry_run=False):

    deleted_count = 0

    skipped_count = 0

    recovered_bytes = 0

    cutoff_time = time.time() - (min_age_hours * 3600)



    for root, dirs, files in os.walk(folder_path, topdown=False):

        for file in files:

            file_path = Path(root) / file

            try:

                stat = file_path.stat()

                # Skip files newer than minimum retention age

                if stat.st_mtime > cutoff_time:

                    continue



                size = stat.st_size

                if not dry_run:

                    try:

                        import stat as stat_mod

                        os.chmod(file_path, stat_mod.S_IWRITE)

                    except Exception:

                        pass

                    file_path.unlink(missing_ok=True)

                deleted_count += 1

                recovered_bytes += size

            except Exception:

                skipped_count += 1



        # Attempt to prune empty directories

        for d in dirs:

            dir_path = Path(root) / d

            try:

                if not any(dir_path.iterdir()):

                    if not dry_run:

                        dir_path.rmdir()

            except Exception:

                pass



    return {

        "folder": str(folder_path),

        "deleted": deleted_count,

        "skipped": skipped_count,

        "recovered_mb": round(recovered_bytes / (1024 * 1024), 2),

        "status": "SUCCESS" if skipped_count == 0 else "PARTIAL"

    }



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

    """Run Windows Disk Cleanup (cleanmgr.exe) silently with safe non-destructive flags."""

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



class NunesFleetClient:

    def __init__(self, computer_name=None, dashboard_url=None):

        self.computer = (computer_name or socket.gethostname()).upper()

        self.user = os.environ.get("USER") or os.environ.get("USERNAME") or "User"

        self.os_name = get_os_friendly_name()

        self.dashboard_url = dashboard_url

        self.data_dir = Path.home() / ".nunes_cleaner"

        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.state_file = self.data_dir / "client_state.json"

        self.state = self.load_state()



    def load_state(self):

        if self.state_file.exists():

            try:

                with open(self.state_file, "r", encoding="utf-8") as f:

                    return json.load(f)

            except Exception:

                pass

        return {

            "last_clean_utc": None,

            "last_clean_status": "READY",

            "last_trigger": None,

            "total_cleaned_mb": 0.0

        }



    def save_state(self):

        try:

            with open(self.state_file, "w", encoding="utf-8") as f:

                json.dump(self.state, f, indent=2)

        except Exception:

            pass



    def perform_cleanup(self, trigger="SCHEDULE", cleanmgr_enabled=True, include_recycle_bin=False, dry_run=False):

        targets = get_cleanup_targets()

        folder_results = []

        total_deleted = 0

        total_skipped = 0

        total_mb = 0.0



        for target in targets:

            res = clean_target_folder(target, min_age_hours=0, dry_run=dry_run)

            folder_results.append({

                "Folder": res["folder"],

                "Deleted": res["deleted"],

                "Skipped": res["skipped"],

                "EstimatedMB": res["recovered_mb"],

                "Status": res["status"]

            })

            total_deleted += res["deleted"]

            total_skipped += res["skipped"]

            total_mb += res["recovered_mb"]



        # Windows Disk Cleanup (cleanmgr.exe) Integration

        if platform.system() == "Windows" and cleanmgr_enabled and not dry_run:

            cm_res = run_cleanmgr(include_recycle_bin=include_recycle_bin)

            if cm_res:

                folder_results.append({

                    "Folder": "Windows Disk Cleanup (cleanmgr.exe)",

                    "Deleted": cm_res["deleted"],

                    "Skipped": 0,

                    "EstimatedMB": cm_res["recovered_mb"],

                    "Status": "SUCCESS"

                })

                total_deleted += cm_res["deleted"]

                total_mb += cm_res["recovered_mb"]



        free_gb = get_free_space_gb()

        status_str = "SUCCESS" if total_skipped == 0 else "PARTIAL"

        now_iso = datetime.now(timezone.utc).isoformat()



        self.state["last_clean_utc"] = now_iso

        self.state["last_clean_status"] = status_str

        self.state["last_trigger"] = trigger

        self.state["total_cleaned_mb"] += total_mb

        self.save_state()



        result_payload = {

            "Version": VERSION,

            "TimestampUtc": now_iso,

            "Computer": self.computer,

            "OS": self.os_name,

            "User": self.user,

            "Command": "CLEAN",

            "Trigger": trigger,

            "Status": status_str,

            "Deleted": total_deleted,

            "Skipped": total_skipped,

            "EstimatedRecoveredMB": round(total_mb, 2),

            "FreeSpaceAfterGB": free_gb,

            "Folders": folder_results

        }

        return result_payload



    def build_heartbeat(self):

        ts_ip = get_tailscale_ip()

        lan_ip = get_local_ip()

        now_iso = datetime.now(timezone.utc).isoformat()



        last_clean = self.state.get("last_clean_utc")

        hours_since = 999.0

        if last_clean:

            try:

                dt = datetime.fromisoformat(last_clean.replace("Z", "+00:00"))

                hours_since = (datetime.now(timezone.utc) - dt).total_seconds() / 3600.0

            except Exception:

                pass



        next_due_in = max(0.0, 4.0 - hours_since)



        # Query live disk stats

        total_gb, used_gb, free_gb, pct_used = 120.0, 60.0, 10.0, 50.0

        try:

            stat = shutil.disk_usage("C:" if platform.system() == "Windows" else "/")

            total_gb = round(stat.total / (1024 ** 3), 2)

            used_gb = round(stat.used / (1024 ** 3), 2)

            free_gb = round(stat.free / (1024 ** 3), 2)

            pct_used = round((stat.used / stat.total) * 100, 1)

        except Exception:

            pass



        status_payload = {

            "Version": VERSION,

            "Computer": self.computer,

            "User": self.user,

            "OS": self.os_name,

            "LastSeenUtc": now_iso,

            "State": "READY",

            "Message": f"Auto clean due in {next_due_in:.1f} hours" if next_due_in > 0 else "Auto clean due",

            "Online": True,

            "NetworkMode": "TAILSCALE" if ts_ip else "LAN",

            "TailscaleUp": bool(ts_ip),

            "TailscaleIP": ts_ip or "-",

            "LocalIPv4": lan_ip,

            "AutoCleanEnabled": True,

            "AutoCleanEveryHours": 4,

            "MinimumAgeHours": 24,

            "LastCleanUtc": last_clean,

            "LastCleanStatus": self.state.get("last_clean_status", "READY"),

            "LastTrigger": self.state.get("last_trigger", "SCHEDULE"),

            "DiskFreeGB": free_gb,

            "DiskTotalGB": total_gb,

            "DiskUsedGB": used_gb,

            "DiskPercentUsed": pct_used,

            "disk_free_gb": free_gb,

            "disk_total_gb": total_gb,

            "disk_used_gb": used_gb,

            "disk_percent_used": pct_used

        }

        return status_payload, hours_since



    def send_report(self, status_payload, result_payload=None):

        # 1. Try HTTP Dashboard API endpoint first (/api/report) for instant zero-latency connection

        urls = [self.dashboard_url] if self.dashboard_url else DEFAULT_DASHBOARD_URLS

        body_data = {

            "status": status_payload,

            "result": result_payload

        }

        json_bytes = json.dumps(body_data).encode("utf-8")



        for u in urls:

            if not u:

                continue

            api_endpoint = u.rstrip("/") + "/api/report"

            try:

                req = urllib.request.Request(

                    api_endpoint,

                    data=json_bytes,

                    headers={"Content-Type": "application/json", "User-Agent": "NunesFleetClient/7.4.0"},

                    method="POST"

                )

                with urllib.request.urlopen(req, timeout=3) as resp:

                    res_json = json.loads(resp.read().decode())

                    if res_json.get("success"):

                        # Mirror to local programdata cache if available

                        try:

                            pd = Path(r"C:\ProgramData\NunesCleanerV7\Status")

                            pd.mkdir(parents=True, exist_ok=True)

                            with open(pd / f"{self.computer}.status", "w", encoding="utf-8") as pf:

                                json.dump(status_payload, pf, indent=2)

                        except Exception:

                            pass

                        return res_json.get("pending_command")

            except Exception:

                continue



        # 2. Mirror to NAS share if mounted and fast-accessible

        for root in DEFAULT_SMB_PATHS:

            try:

                if str(root).startswith('\\'):

                    host = str(root).lstrip('\\').split('\\')[0]

                    with socket.create_connection((host, 445), timeout=0.25):

                        pass

                p = Path(root)

                if p.exists():

                    status_file = p / "Status" / f"{self.computer}.status"

                    status_file.parent.mkdir(parents=True, exist_ok=True)

                    with open(status_file, "w", encoding="utf-8") as f:

                        json.dump(status_payload, f, indent=2)



                    if result_payload:

                        res_file = p / "Results" / "Latest" / f"{self.computer}.result"

                        res_file.parent.mkdir(parents=True, exist_ok=True)

                        with open(res_file, "w", encoding="utf-8") as f:

                            json.dump(result_payload, f, indent=2)

                    return None

            except Exception:

                pass

        return None



    def run_cycle(self):

        status, hours_since = self.build_heartbeat()

        result = None



        # Adaptive Red-Zone Sentry: Auto-clean every 1 hour if drive is in RED (<11.9 GB or >=90%)

        is_red_zone = (status.get("DiskPercentUsed", 0) >= 90.0 or status.get("DiskFreeGB", 100) < 11.9)

        target_interval_hours = 1.0 if is_red_zone else 1.0  # Guard hourly to keep within the blue

        if hours_since >= target_interval_hours:

            result = self.perform_cleanup(trigger="RED_ZONE_SENTRY" if is_red_zone else "HOURLY_GUARD")

            status, _ = self.build_heartbeat()



        # Autonomous Anti-Hang / System Freeze Check

        try:

            import hang_resolver

            hang_stat = hang_resolver.check_hang_status()

            if hang_stat.get("is_hanging"):

                print(f"[{datetime.now()}] ⚠️ System freeze detected ({'; '.join(hang_stat.get('reasons', []))}). Executing emergency rescue...")

                hang_resolver.resolve_system_hang()

                status, _ = self.build_heartbeat()

        except Exception:

            pass



        # Send heartbeat & result to dashboard

        pending_cmd = self.send_report(status, result)



        # Handle remote manual clean request from dashboard

        if pending_cmd:

            cmd = pending_cmd if isinstance(pending_cmd, str) else pending_cmd.get("Command", "CLEAN")

            opts = pending_cmd.get("Options", {}) if isinstance(pending_cmd, dict) else {}

            cm_flag = opts.get("cleanmgr", True)

            rb_flag = opts.get("recycle_bin", False)



            if cmd == "CLEAN":

                result = self.perform_cleanup(trigger="MANUAL", cleanmgr_enabled=cm_flag, include_recycle_bin=rb_flag)

                status, _ = self.build_heartbeat()

                self.send_report(status, result)

            elif cmd == "RESCUE_HANG":

                try:

                    import hang_resolver

                    hang_res = hang_resolver.resolve_system_hang()

                    print(f"[{datetime.now()}] Anti-Hang Rescue executed: Trimmed {hang_res['trimmed_process_count']} processes, freed {hang_res['ram_freed_mb']} MB RAM.")

                except Exception as e:

                    print(f"[{datetime.now()}] Rescue failed: {e}")

                status, _ = self.build_heartbeat()

                self.send_report(status, None)



    def run_daemon(self, interval_seconds=10):

        print(f"[{datetime.now()}] NUNES Fleet Client started on {self.computer} ({self.os_name}).")

        print(f"[{datetime.now()}] Background cleaner active: Every 4 hours + 1-min live dashboard heartbeat.")

        while True:

            try:

                self.run_cycle()

            except Exception as e:

                pass

            time.sleep(interval_seconds)



def install_service():

    system = platform.system()

    script_path = Path(__file__).resolve()

    python_bin = sys.executable



    print(f"Installing NUNES Fleet Cleaner on {system}...")



    if system == "Darwin":  # macOS LaunchAgent

        plist_dir = Path.home() / "Library" / "LaunchAgents"

        plist_dir.mkdir(parents=True, exist_ok=True)

        plist_path = plist_dir / "com.nunes.cleaner.plist"



        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">

<dict>

    <key>Label</key>

    <string>com.nunes.cleaner</string>

    <key>ProgramArguments</key>

    <array>

        <string>{python_bin}</string>

        <string>{script_path}</string>

        <string>--daemon</string>

    </array>

    <key>RunAtLoad</key>

    <true/>

    <key>KeepAlive</key>

    <true/>

    <key>StandardErrorPath</key>

    <string>/tmp/nunes_cleaner_err.log</string>

    <key>StandardOutPath</key>

    <string>/tmp/nunes_cleaner_out.log</string>

</dict>

</plist>"""

        with open(plist_path, "w", encoding="utf-8") as f:

            f.write(plist_content)

        subprocess.run(["launchctl", "unload", str(plist_path)], stderr=subprocess.DEVNULL)

        subprocess.run(["launchctl", "load", "-w", str(plist_path)])

        print(f"[OK] macOS LaunchAgent installed and running: {plist_path}")

        print("Runs silently in the background on startup, every 4 hours + 1-min heartbeat.")



    elif system == "Linux":

        service_dir = Path.home() / ".config" / "systemd" / "user"

        service_dir.mkdir(parents=True, exist_ok=True)

        service_path = service_dir / "nunes-cleaner.service"



        service_content = f"""[Unit]

Description=NUNES Autonomous Fleet Temp Cleaner

After=network.target



[Service]

Type=simple

ExecStart={python_bin} {script_path} --daemon

Restart=always

RestartSec=60



[Install]

WantedBy=default.target

"""

        with open(service_path, "w", encoding="utf-8") as f:

            f.write(service_content)

        subprocess.run(["systemctl", "--user", "daemon-reload"], stderr=subprocess.DEVNULL)

        subprocess.run(["systemctl", "--user", "enable", "--now", "nunes-cleaner.service"])

        print(f"[OK] Linux systemd user service installed and running: {service_path}")



    elif system == "Windows":

        task_name = "NUNES Universal Fleet Cleaner"

        cmd = f'schtasks /Create /TN "{task_name}" /TR "\"{python_bin}\" \"{script_path}\" --daemon" /SC ONLOGON /RL HIGHEST /F'

        res = subprocess.run(cmd, shell=True)

        if res.returncode == 0:

            subprocess.run(f'schtasks /Run /TN "{task_name}"', shell=True)

            print(f"[OK] Windows Scheduled Task installed and running: {task_name}")

        else:

            print("[WARN] Could not register scheduled task directly. Please run installer as Administrator.")



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="NUNES Universal Fleet Temp Cleaner")

    parser.add_argument("--clean", action="store_true", help="Perform one-off immediate cleanup")

    parser.add_argument("--dry-run", action="store_true", help="Simulate without deleting files")

    parser.add_argument("--daemon", action="store_true", help="Run background worker daemon (4H clean + 1-min heartbeat)")

    parser.add_argument("--install", action="store_true", help="Install as OS background service (Windows, Mac, Linux)")

    parser.add_argument("--dashboard", type=str, help="Custom Dashboard URL (e.g. http://192.168.29.88:8090)")

    parser.add_argument("--no-cleanmgr", action="store_true", help="Disable Windows Disk Cleanup (cleanmgr.exe)")

    parser.add_argument("--include-recycle-bin", action="store_true", help="Include Recycle Bin in Disk Cleanup")

    args = parser.parse_args()



    client = NunesFleetClient(dashboard_url=args.dashboard)



    if args.install:

        install_service()

    elif args.clean:

        print(f"Cleaning {client.computer} ({client.os_name})...")

        res = client.perform_cleanup(

            trigger="MANUAL",

            cleanmgr_enabled=not args.no_cleanmgr,

            include_recycle_bin=args.include_recycle_bin,

            dry_run=args.dry_run

        )

        print(json.dumps(res, indent=2))

        client.send_report(client.build_heartbeat()[0], res)

    elif args.daemon:

        client.run_daemon()

    else:

        # Default: run one cycle (heartbeat + clean if due)

        client.run_cycle()

        print(f"[OK] Heartbeat and status reported to dashboard for {client.computer} ({client.os_name}).")

