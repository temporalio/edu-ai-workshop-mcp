#!/bin/bash
set -e

# Install dependencies for uv and Python setup first
curl -LsSf https://astral.sh/uv/install.sh | sh
. $HOME/.cargo/env
uv sync
uv pip install ipykernel jupyter
uv run python -m ipykernel install --user --name='python3' --display-name='Python 3 (ipykernel)'

# Download and install Claude Desktop
echo "Installing Claude Desktop..."
cd /tmp
wget -O claude.deb "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest-win-x64/Claude-Setup-x64.exe" || \
wget -O claude.deb "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop_latest_amd64.deb"

# Install Claude Desktop
sudo apt-get update
sudo apt-get install -y ./claude.deb || true

# Alternative: Install via AppImage if .deb fails
if [ ! -f /usr/bin/claude ] && [ ! -f /opt/Claude/claude ]; then
    echo "Trying AppImage installation..."
    wget -O /tmp/Claude.AppImage "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop_latest_x86_64.AppImage"
    chmod +x /tmp/Claude.AppImage
    sudo mv /tmp/Claude.AppImage /usr/local/bin/claude
fi

echo "Claude Desktop installation complete!"
echo "Access the desktop environment at port 6080 to use Claude Desktop"