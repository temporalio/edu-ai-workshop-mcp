#!/bin/bash
set -e

echo "=== Workshop Setup (runs once) ==="
exec > >(tee -a /tmp/setup.log) 2>&1

# Temporal CLI
echo "[1/5] Installing Temporal CLI..."
curl -sSf https://temporal.download/cli.sh | sh

# Python
echo "[2/5] Installing Python dependencies..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv sync
uv pip install ipykernel jupyter
uv run python -m ipykernel install --user --name='python3' --display-name='Python 3 (ipykernel)'

# Desktop environment
echo "[3/5] Installing desktop environment..."
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    fluxbox x11vnc novnc websockify xterm x11-utils dbus-x11 xvfb

# Claude Desktop
echo "[4/5] Downloading Claude Desktop (200MB, ~2 min)..."
cd /tmp
timeout 300 wget -q --show-progress -O claude.deb \
    "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop-linux-x64-latest.deb" || {
    echo "ERROR: Claude Desktop download failed"
    exit 1
}

echo "[5/5] Installing Claude Desktop..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ./claude.deb
rm claude.deb

echo "Setup complete!"