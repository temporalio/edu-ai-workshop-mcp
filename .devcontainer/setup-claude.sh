#!/bin/bash
set -e

echo "=== Starting Claude Desktop setup ==="
exec > >(tee -a /tmp/setup-claude.log) 2>&1

# Python setup
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

echo "Running uv sync..."
uv sync

echo "Installing Jupyter kernel..."
uv pip install ipykernel jupyter
uv run python -m ipykernel install --user --name='python3' --display-name='Python 3 (ipykernel)'

# Desktop install
echo "Installing desktop environment..."
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    fluxbox tigervnc-standalone-server novnc websockify xterm \
    x11-utils dbus-x11

# VNC setup
echo "Configuring VNC..."
mkdir -p ~/.vnc
echo "temporal" | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd

cat > ~/.vnc/xstartup << 'EOF'
#!/bin/bash
exec fluxbox &
EOF
chmod +x ~/.vnc/xstartup

# Create desktop start script
cat > ~/start-desktop.sh << 'EOF'
#!/bin/bash
# Kill any existing VNC servers
vncserver -kill :1 2>/dev/null || true
sleep 1

# Start VNC server
vncserver :1 -geometry 1280x720 -depth 24

# Start noVNC
websockify --web=/usr/share/novnc 6080 localhost:5901 &
EOF
chmod +x ~/start-desktop.sh

# Download Claude Desktop with timeout
echo "Downloading Claude Desktop (this may take a minute)..."
cd /tmp

# Try with timeout
timeout 180 wget -q --show-progress -O claude.deb \
    "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop-linux-x64-latest.deb" || \
timeout 180 curl -L --progress-bar -o claude.deb \
    "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop-linux-x64-latest.deb" || \
echo "⚠️  Claude download failed or timed out - you can install it manually later"

# Install if download succeeded
if [ -f claude.deb ] && [ -s claude.deb ]; then
    echo "Installing Claude Desktop..."
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ./claude.deb || \
        echo "⚠️  Claude installation failed - continuing anyway"
    rm claude.deb
else
    echo "⚠️  Claude Desktop not installed - skipping"
fi

echo "=== Setup complete! Check /tmp/setup-claude.log for details ==="
