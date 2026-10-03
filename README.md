Autonomous System Temp Cleaner

    Purpose: A lightweight, silent background utility that automatically clears Windows temporary directories every 4 hours to maintain peak system performance.

    Tech Stack: Python (ctypes, os, shutil, schedule), Windows Task Scheduler wrapper, or a compiled .pyw background script.

    Key Features:

        Targeted Purging: Safely sweeps C:\Windows\Temp, %USERPROFILE%\AppData\Local\Temp, and browser cache directories.

        Background Daemon: Runs silently in the system tray or via a scheduled Windows background task every 4 hours without interrupting active workflows.

        Exception Handling: Gracefully skips locked files currently in use by active applications without throwing blocking errors.



Yes. I checked the repository and rebuilt it into a more complete GitHub-ready project.

The improved project now includes:

- `NUNES_CACHE_CLEANER.bat` — safer V3 cleaner
- `INSTALL.bat` — installs Windows Scheduled Task
- `STATUS.bat` — shows last run / next run / result
- `RUN_NOW.bat` — manually triggers the scheduled cleaner
- `UNINSTALL.bat` — completely removes the automation
- `README.md` — professional GitHub documentation
- `.gitignore`
- `NUNES_CACHE_CLEANER_V3_RELEASE.zip` — ready for a GitHub Release
- Automatic execution **every 4 hours**
- Automatic execution at **Windows startup**
- Runs hidden as **SYSTEM**
- Basic safety protection against accidentally cleaning dangerous paths such as `C:\` or the user's whole profile

### Download the finished GitHub project

NUNES_CACHE_CLEANER_GITHUB_PROJECT.zip[Download NUNES_CACHE_CLEANER_GITHUB_PROJECT.zip](sandbox:/mnt/data/NUNES_CACHE_CLEANER_GITHUB_PROJECT.zip)

You can also get the ready-to-distribute release ZIP:

NUNES_CACHE_CLEANER_V3_RELEASE.zip[Download NUNES_CACHE_CLEANER_V3_RELEASE.zip](sandbox:/mnt/data/NUNES_CACHE_CLEANER_GITHUB_PROJECT/NUNES_CACHE_CLEANER_V3_RELEASE.zip)

### Now update your GitHub repository

Your current repository is:

[Autonomous-System-Temp-Cleaner GitHub repository](https://github.com/AbishekPranavGV/Autonomous-System-Temp-Cleaner?utm_source=chatgpt.com)

Extract my `NUNES_CACHE_CLEANER_GITHUB_PROJECT.zip`, open that folder in PowerShell, and run:

```powershell
git clone https://github.com/AbishekPranavGV/Autonomous-System-Temp-Cleaner.git
cd Autonomous-System-Temp-Cleaner
```

Copy these new files into that folder, replacing the old versions where applicable.

Then:

```powershell
git add .
git commit -m "NUNES Cache Cleaner V3 - complete 4 hour automation"
git push origin main
```

After pushing, your repository should look approximately like:

```text
Autonomous-System-Temp-Cleaner
│
├── NUNES_CACHE_CLEANER.bat
├── INSTALL.bat
├── RUN_NOW.bat
├── STATUS.bat
├── UNINSTALL.bat
├── README.md
├── .gitignore
└── NUNES_CACHE_CLEANER_V3_RELEASE.zip
```

I also recommend creating a GitHub **Release** called:

```text
NUNES Cache Cleaner v3.0
```

and attaching:

```text
NUNES_CACHE_CLEANER_V3_RELEASE.zip
```

One limitation: the GitHub connection available to me currently reports **read-only access**, so I couldn't directly commit these changes into `AbishekPranavGV/Autonomous-System-Temp-Cleaner`. The project files themselves are finished and ready for you to push.
