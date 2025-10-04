#!/bin/bash
set -e

echo "=== Installing Claude Desktop (background) ==="
exec > >(tee -a /tmp/setup-desktop.log) 2>&1

# Desktop environment
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    fluxbox x11vnc novnc websockify xterm x11-utils dbus-x11 xvfb

# Create desktop start script
cat > ~/start-desktop.sh << 'EOF'
#!/bin/bash
pkill -f x11vnc 2>/dev/null || true
pkill -f Xvfb 2>/dev/null || true
pkill -f websockify 2>/dev/null || true
sleep 1

Xvfb :1 -screen 0 1280x720x24 >/dev/null 2>&1 &
export DISPLAY=:1
sleep 2

fluxbox >/dev/null 2>&1 &
sleep 1

x11vnc -display :1 -nopw -forever -shared -rfbport 5901 >/dev/null 2>&1 &
sleep 2

websockify --web=/usr/share/novnc 6080 localhost:5901 >/tmp/novnc.log 2>&1 &

echo "Desktop ready at: https://$CODESPACE_NAME-6080.preview.app.github.dev"
EOF
chmod +x ~/start-desktop.sh

# Download and install Claude Desktop
cd /tmp
timeout 240 wget -q -O claude.deb \
    "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop-linux-x64-latest.deb" 2>/dev/null || exit 0

if [ -f claude.deb ] && [ -s claude.deb ]; then
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ./claude.deb
    rm claude.deb
    echo "Claude Desktop installed and ready!"
fi