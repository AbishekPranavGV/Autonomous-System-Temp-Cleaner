#!/bin/bash
# ==============================================================================
# NUNES Fleet Temp Cleaner - macOS Automatic Service Installer
# Installs a native macOS LaunchAgent running every 4 hours + 1-min live heartbeat.
# ==============================================================================

set -e

echo "=============================================================="
echo "    NUNES FLEET TEMP CLEANER - macOS INSTALLER"
echo "=============================================================="
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is required. Please install Python 3 or Xcode Command Line Tools."
    exit 1
fi

INSTALL_DIR="$HOME/.nunes_cleaner"
mkdir -p "$INSTALL_DIR"

SCRIPT_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/nunes_universal_cleaner.py"

if [ -f "$SCRIPT_SOURCE" ]; then
    cp "$SCRIPT_SOURCE" "$INSTALL_DIR/nunes_universal_cleaner.py"
else
    # Fallback: download or locate via mounted NAS
    echo "[..] Locating universal cleaner script..."
    if [ -f "/Volumes/Common/Completed/Abishek/final/NUNES_TEMP_final/NUNES_TEMP_CLEANER_V7_4_0_HEARTBEAT_RECOVERY/nunes_universal_cleaner.py" ]; then
        cp "/Volumes/Common/Completed/Abishek/final/NUNES_TEMP_final/NUNES_TEMP_CLEANER_V7_4_0_HEARTBEAT_RECOVERY/nunes_universal_cleaner.py" "$INSTALL_DIR/nunes_universal_cleaner.py"
    fi
fi

chmod +x "$INSTALL_DIR/nunes_universal_cleaner.py"

# Run self-installation
echo "[..] Registering LaunchAgent background daemon..."
python3 "$INSTALL_DIR/nunes_universal_cleaner.py" --install

# Send initial heartbeat
echo "[..] Sending initial heartbeat to central dashboard..."
python3 "$INSTALL_DIR/nunes_universal_cleaner.py"

echo ""
echo "=============================================================="
echo " [OK] SUCCESS! NUNES Cleaner is now active on this Mac."
echo " - Automatic cleaning: Every 4 hours"
echo " - Live dashboard heartbeat: Every 1 minute"
echo " - View status: http://192.168.29.88:8090"
echo "=============================================================="
