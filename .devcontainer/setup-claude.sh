#!/bin/bash
set -e

# Install uv (it's fast)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Python setup (keep this - needed for your workshop)
uv sync
uv pip install ipykernel jupyter
uv run python -m ipykernel install --user --name='python3' --display-name='Python 3 (ipykernel)'

# Install ONLY essential desktop packages (this is the slow part)
echo "Installing desktop environment..."
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    fluxbox \
    tigervnc-standalone-server \
    novnc \
    websockify \
    xterm

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

# Download Claude Desktop (background this to not block)
echo "Downloading Claude Desktop..."
(
  cd /tmp
  wget -q -O claude.deb "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop_latest_amd64.deb" && \
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ./claude.deb
) &

# Create startup script while Claude downloads
cat > ~/start-desktop.sh << 'EOF'
#!/bin/bash
vncserver -kill :1 2>/dev/null || true
vncserver :1 -geometry 1920x1080 -depth 24 -localhost no
websockify -D --web=/usr/share/novnc/ 6080 localhost:5901
EOF
chmod +x ~/start-desktop.sh

echo "Setup complete! Claude Desktop installing in background..."