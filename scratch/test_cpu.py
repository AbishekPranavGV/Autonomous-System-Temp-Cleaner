import ctypes
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", ctypes.c_uint32), ("dwHighDateTime", ctypes.c_uint32)]

def filetime_to_int(ft):
    return (ft.dwHighDateTime << 32) + ft.dwLowDateTime

idle1, kern1, user1 = FILETIME(), FILETIME(), FILETIME()
idle2, kern2, user2 = FILETIME(), FILETIME(), FILETIME()

k32 = ctypes.windll.kernel32
if k32.GetSystemTimes(ctypes.byref(idle1), ctypes.byref(kern1), ctypes.byref(user1)):
    time.sleep(0.15)
    if k32.GetSystemTimes(ctypes.byref(idle2), ctypes.byref(kern2), ctypes.byref(user2)):
        idle = filetime_to_int(idle2) - filetime_to_int(idle1)
        kern = filetime_to_int(kern2) - filetime_to_int(kern1)
        user = filetime_to_int(user2) - filetime_to_int(user1)
        total = kern + user
        if total > 0:
            cpu_pct = round(((total - idle) / total) * 100, 1)
            print(f"Deterministic Win32 CPU Load: {max(0.0, min(100.0, cpu_pct))}%")
