#!/bin/bash
set -e

echo "=== Starting Workshop Services ==="
exec > >(tee -a /tmp/startup.log) 2>&1

# Export paths
export PATH="$HOME/.temporalio/bin:$HOME/.local/bin:$PATH"

# Start Temporal
echo "Starting Temporal..."
temporal server start-dev --ui-port 8080 >/tmp/temporal.log 2>&1 &
sleep 3

# Start MCP server
echo "Starting MCP server..."
cd /workspaces/edu-ai-workshop-mcp
uv run python mcp_servers/weather.py > /tmp/mcp-server.log 2>&1 &

# Start desktop
echo "Starting desktop..."
pkill -f x11vnc 2>/dev/null || true
pkill -f Xvfb 2>/dev/null || true
pkill -f websockify 2>/dev/null || true
sleep 1

Xvfb :1 -screen 0 1280x720x24 >/dev/null 2>&1 &
export DISPLAY=:1
sleep 2

fluxbox >/dev/null 2>&1 &
x11vnc -display :1 -nopw -forever -shared -rfbport 5901 >/dev/null 2>&1 &
sleep 1

websockify --web=/usr/share/novnc 6080 localhost:5901 >/tmp/novnc.log 2>&1 &

# Set port visibility
gh codespace ports visibility 5125:public -c $CODESPACE_NAME 2>/dev/null || true
gh codespace ports visibility 6080:public -c $CODESPACE_NAME 2>/dev/null || true
gh codespace ports visibility 8080:public -c $CODESPACE_NAME 2>/dev/null || true

echo "All services started!"
echo "   Temporal UI: https://$CODESPACE_NAME-8080.preview.app.github.dev"
echo "   Claude Desktop: https://$CODESPACE_NAME-6080.preview.app.github.dev"