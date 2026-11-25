#!/bin/bash
# ==============================================================================
# NUNES Fleet Temp Cleaner - Linux Automatic Service Installer
# Installs a systemd user daemon running every 4 hours + 1-min live heartbeat.
# ==============================================================================

set -e

echo "=============================================================="
echo "    NUNES FLEET TEMP CLEANER - LINUX INSTALLER"
echo "=============================================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is required. Please install python3 (e.g. sudo apt install python3)."
    exit 1
fi

INSTALL_DIR="$HOME/.nunes_cleaner"
mkdir -p "$INSTALL_DIR"

SCRIPT_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/nunes_universal_cleaner.py"

if [ -f "$SCRIPT_SOURCE" ]; then
    cp "$SCRIPT_SOURCE" "$INSTALL_DIR/nunes_universal_cleaner.py"
fi

chmod +x "$INSTALL_DIR/nunes_universal_cleaner.py"

# Run self-installation
echo "[..] Registering systemd user daemon..."
python3 "$INSTALL_DIR/nunes_universal_cleaner.py" --install

# Send initial heartbeat
echo "[..] Sending initial heartbeat to central dashboard..."
python3 "$INSTALL_DIR/nunes_universal_cleaner.py"

echo ""
echo "=============================================================="
echo " [OK] SUCCESS! NUNES Cleaner is now active on this Linux PC."
echo " - Automatic cleaning: Every 4 hours"
echo " - Live dashboard heartbeat: Every 1 minute"
echo " - View status: http://192.168.29.88:8090"
echo "=============================================================="
