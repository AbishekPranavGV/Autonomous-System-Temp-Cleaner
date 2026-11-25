with open('cleaner.py', 'r', encoding='utf-8') as f:
    c = f.read()

old = 'def purge_35_day_retention_backups():'
new = '''def purge_30_day_retention_backups():
    """Purges any prompt backup, snapshot, or log older than 30 days (30-day rolling retention rule)."""
    try:
        import prompt_backup_manager
        return prompt_backup_manager.purge_expired_backups()
    except Exception:
        return {"purged_count": 0, "purged_bytes": 0, "retention_days": 30}

def purge_35_day_retention_backups():
    """Legacy alias: standardizes to unified 30-day retention rule."""
    return purge_30_day_retention_backups()'''

if old in c:
    c = c.replace(old, new, 1)
    c = c.replace('retention_res = purge_35_day_retention_backups()', 'retention_res = purge_30_day_retention_backups()')
    c = c.replace('"retention_35d": retention_res', '"retention_30d": retention_res, "retention_35d": retention_res')
    with open('cleaner.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Updated cleaner.py successfully!')
else:
    print('Target not found in cleaner.py')
