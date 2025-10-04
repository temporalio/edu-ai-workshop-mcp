#!/bin/bash
set -e

# Python setup
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv sync
uv pip install ipykernel jupyter
uv run python -m ipykernel install --user --name='python3' --display-name='Python 3 (ipykernel)'

# Desktop install
echo "Installing desktop environment..."
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    fluxbox tigervnc-standalone-server novnc websockify xterm

# VNC setup
mkdir -p ~/.vnc
echo "temporal" | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd

cat > ~/.vnc/xstartup << 'EOF'
#!/bin/bash
exec fluxbox &
EOF
chmod +x ~/.vnc/xstartup

# Download Claude Desktop using the official download link
echo "Downloading Claude Desktop..."
cd /tmp
# This redirects to the latest version
wget -O claude.deb "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop-linux-x64-latest.deb" 2>/dev/null || \
curl -L -o claude.deb "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop-linux-x64-latest.deb" || \
echo "Claude download failed, skipping..."

if [ -f claude.deb ]; then
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ./claude.deb || echo "Claude installation failed"
fi

cat > ~/start-de