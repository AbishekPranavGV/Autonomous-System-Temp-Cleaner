"""
NUNES PROMPT & SYSTEM STATE BACKUP MANAGER (30-Day Unified Retention)
=====================================================================
1. Captures and persists full user prompt instructions, execution state,
   and system diagnostic snapshots.
2. Enforces a strict 30-day retention lifecycle: files, snapshots, and
   prompt archives older than 30 days (2,592,000 seconds) are automatically
   purged once every 30-day rolling cycle (configurable).
3. Universal compatibility: Windows 7, 8, 10, 11 and Windows Server.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

DEFAULT_RETENTION_DAYS = 30
RETENTION_DAYS = int(os.environ.get("BACKUP_RETENTION_DAYS", DEFAULT_RETENTION_DAYS))
RETENTION_SECONDS = RETENTION_DAYS * 86400  # 2,592,000 seconds for 30 days

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "dashboard" / "data"
PROMPT_BACKUP_DIR = DATA_DIR / "prompt_backups"
PROGRAM_DATA_BACKUP_DIR = Path(os.environ.get("ProgramData", "C:/ProgramData")) / "NunesCleanerV7" / "PromptBackups"

def ensure_dirs():
    PROMPT_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    try:
        PROGRAM_DATA_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

def backup_prompt(prompt_text, metadata=None):
    """Saves a prompt entry with creation timestamp, expiration, and metadata."""
    ensure_dirs()
    now_dt = datetime.now(timezone.utc)
    now_ts = now_dt.timestamp()
    expire_dt = now_dt + timedelta(days=RETENTION_DAYS)
    
    clean_id = f"prompt_{now_dt.strftime('%Y%m%d_%H%M%S')}_{int(now_ts * 1000) % 1000:03d}"
    
    payload = {
        "id": clean_id,
        "created_at_utc": now_dt.isoformat(),
        "created_timestamp": now_ts,
        "expires_at_utc": expire_dt.isoformat(),
        "expires_timestamp": expire_dt.timestamp(),
        "retention_days": RETENTION_DAYS,
        "prompt": prompt_text,
        "metadata": metadata or {},
        "status": "BACKED_UP"
    }

    # Save to local project data
    out_file = PROMPT_BACKUP_DIR / f"{clean_id}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    # Mirror to ProgramData for system-wide persistence
    try:
        pd_file = PROGRAM_DATA_BACKUP_DIR / f"{clean_id}.json"
        with open(pd_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except Exception:
        pass

    return payload

def list_prompt_backups():
    """Returns list of active prompt backups with remaining days and status."""
    ensure_dirs()
    now_ts = time.time()
    backups = []
    
    # Read from PROMPT_BACKUP_DIR
    if PROMPT_BACKUP_DIR.exists():
        for fp in sorted(PROMPT_BACKUP_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    entry = json.load(f)
                    created_ts = entry.get("created_timestamp", fp.stat().st_mtime)
                    age_seconds = now_ts - created_ts
                    age_days = round(age_seconds / 86400, 1)
                    days_remaining = max(0.0, round(RETENTION_DAYS - age_days, 1))
                    
                    entry["age_days"] = age_days
                    entry["days_remaining"] = days_remaining
                    entry["is_expired"] = (age_days >= RETENTION_DAYS)
                    backups.append(entry)
            except Exception:
                continue

    return backups

def purge_expired_backups(log_callback=None, max_retention_days=None):
    """Purges any prompt backup or snapshot older than retention limit (default 30-day rolling rule)."""
    limit_days = max_retention_days or RETENTION_DAYS
    limit_seconds = limit_days * 86400
    now_ts = time.time()
    purged_count = 0
    purged_bytes = 0

    scan_dirs = [PROMPT_BACKUP_DIR, PROGRAM_DATA_BACKUP_DIR]
    for d in scan_dirs:
        if not d.exists():
            continue
        try:
            for fp in d.glob("*.json"):
                try:
                    mtime = fp.stat().st_mtime
                    age_seconds = now_ts - mtime
                    if age_seconds >= limit_seconds:
                        sz = fp.stat().st_size
                        fp.unlink(missing_ok=True)
                        purged_count += 1
                        purged_bytes += sz
                        msg = f"🗑️ [30-DAY RETENTION] Purged expired backup: {fp.name} (age: {round(age_seconds/86400, 1)} days)"
                        if log_callback:
                            log_callback(msg, "amber")
                        else:
                            print(msg)
                except Exception:
                    continue
        except Exception:
            continue

    return {
        "purged_count": purged_count,
        "purged_bytes": purged_bytes,
        "retention_days": RETENTION_DAYS
    }

def import_past_prompts():
    """Populates prompt backup storage with all prior prompts from transcript."""
    transcript_path = Path(r"C:\Users\Nunes\.gemini\antigravity\brain\50d997d7-7a4d-4750-9c70-6aed19af6f2b\.system_generated\logs\transcript.jsonl")
    if not transcript_path.exists():
        return 0

    imported = 0
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
                if row.get("type") == "USER_INPUT":
                    content = row.get("content", "").strip()
                    created_at = row.get("created_at")
                    step_idx = row.get("step_index")
                    if content:
                        clean_id = f"prompt_step_{step_idx}"
                        target = PROMPT_BACKUP_DIR / f"{clean_id}.json"
                        if not target.exists():
                            # Parse dt
                            try:
                                dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                            except Exception:
                                dt = datetime.now(timezone.utc)
                            
                            exp_dt = dt + timedelta(days=RETENTION_DAYS)
                            data = {
                                "id": clean_id,
                                "step_index": step_idx,
                                "created_at_utc": dt.isoformat(),
                                "created_timestamp": dt.timestamp(),
                                "expires_at_utc": exp_dt.isoformat(),
                                "expires_timestamp": exp_dt.timestamp(),
                                "retention_days": RETENTION_DAYS,
                                "prompt": content,
                                "metadata": {
                                    "source": "conversation_transcript",
                                    "media": [m.get("uri", "") for m in row.get("media", []) if m.get("uri")]
                                },
                                "status": "BACKED_UP"
                            }
                            ensure_dirs()
                            with open(target, "w", encoding="utf-8") as out_f:
                                json.dump(data, out_f, indent=2)
                            imported += 1
            except Exception:
                continue

    return imported

if __name__ == "__main__":
    ensure_dirs()
    count = import_past_prompts()
    print(f"[OK] Prompt Backup Manager initialized. Imported {count} past prompts.")
    purge_res = purge_expired_backups()
    print(f"[OK] 30-Day Retention Check complete: {purge_res['purged_count']} expired backups removed.")
    active = list_prompt_backups()
    print(f"[OK] Total active prompt backups: {len(active)} (Retained for {RETENTION_DAYS} days).")
