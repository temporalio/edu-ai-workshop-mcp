#!/bin/bash
set -e

# Install dependencies for uv and Python setup first
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv sync
uv pip install ipykernel jupyter
uv run python -m ipykernel install --user --name='python3' --display-name='Python 3 (ipykernel)'

# Install desktop environment and VNC components
echo "Installing desktop environment..."
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    fluxbox \
    tigervnc-standalone-server \
    tigervnc-common \
    novnc \
    websockify \
    xterm \
    wget \
    net-tools

# Set up VNC password
mkdir -p ~/.vnc
echo "temporal" | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd

# Create VNC startup script
cat > ~/.vnc/xstartup << 'EOF'
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec fluxbox &
EOF
chmod +x ~/.vnc/xstartup

# Download and install Claude Desktop
echo "Installing Claude Desktop..."
cd /tmp
wget -O claude.deb "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop_latest_amd64.deb" || true

if [ -f claude.deb ]; then
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ./claude.deb || true
fi

# Alternative: Install via AppImage if .deb fails
if [ ! -f /usr/bin/claude ] && [ ! -f /opt/Claude/claude ]; then
    echo "Trying AppImage installation..."
    wget -O /tmp/Claude.AppImage "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop_latest_x86_64.AppImage" || true
    if [ -f /tmp/Claude.AppImage ]; then
        chmod +x /tmp/Claude.AppImage
        sudo mv /tmp/Claude.AppImage /usr/local/bin/claude
    fi
fi

# Create startup script for VNC+noVNC
cat > ~/start-desktop.sh << 'EOF'
#!/bin/bash
# Kill any existing VNC servers
vncserver -kill :1 2>/dev/null || true

# Start VNC server
vncserver :1 -geometry 1920x1080 -depth 24 -localhost no

# Start noVNC
websockify -D --web=/usr/share/novnc/ 6080 localhost:5901
EOF
chmod +x ~/start-desktop.sh

echo "Setup complete!"
echo "Run ~/start-desktop.sh to start the desktop environment"