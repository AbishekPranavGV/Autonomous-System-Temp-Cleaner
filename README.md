Autonomous System Temp Cleaner

    Purpose: A lightweight, silent background utility that automatically clears Windows temporary directories every 4 hours to maintain peak system performance.

    Tech Stack: Python (ctypes, os, shutil, schedule), Windows Task Scheduler wrapper, or a compiled .pyw background script.

    Key Features:

        Targeted Purging: Safely sweeps C:\Windows\Temp, %USERPROFILE%\AppData\Local\Temp, and browser cache directories.

        Background Daemon: Runs silently in the system tray or via a scheduled Windows background task every 4 hours without interrupting active workflows.

        Exception Handling: Gracefully skips locked files currently in use by active applications without throwing blocking errors.
