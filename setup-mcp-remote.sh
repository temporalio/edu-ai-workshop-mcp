#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "========================================"
echo "MCP Remote Setup Script"
echo "========================================"

# Function to install mcp-remote
install_mcp_remote() {
    echo -e "${YELLOW}Installing mcp-remote...${NC}"
    npm install -g mcp-remote
    echo -e "${GREEN}✓ mcp-remote installed${NC}"
}

# Main execution
echo ""
echo "Installing mcp-remote..."
install_mcp_remote

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""

# Get paths
NODE_PATH=$(which node)
MCP_REMOTE_PATH=$(which mcp-remote)
NPM_ROOT=$(npm root -g)
PROXY_PATH="$NPM_ROOT/mcp-remote/dist/proxy.js"

echo "Detected paths:"
echo "  Node: $NODE_PATH"
echo "  mcp-remote: $MCP_REMOTE_PATH"
echo "  Proxy: $PROXY_PATH"
echo ""
echo "========================================"
echo "CODESPACES Configuration"
echo "========================================"
echo "Add this to claude_desktop_config.json in Codespaces:"
echo ""
echo "{"
echo "    \"mcpServers\": {"
echo "        \"weather\": {"
echo "            \"command\": \"$MCP_REMOTE_PATH\","
echo "            \"args\": ["
echo "                \"<YOUR_CODESPACES_SSE_URL_HERE>\""
echo "            ]"
echo "        }"
echo "    }"
echo "}"
echo ""
echo "========================================"
echo "CLAUDE DESKTOP Configuration"
echo "========================================"
echo "Add this to claude_desktop_config.json on your Mac:"
echo ""
echo "{"
echo "    \"mcpServers\": {"
echo "        \"weather\": {"
echo "            \"command\": \"$NODE_PATH\","
echo "            \"args\": ["
echo "                \"$PROXY_PATH\","
echo "                \"<YOUR_CODESPACES_SSE_URL_HERE>\""
echo "            ]"
echo "        }"
echo "    }"
echo "}"
echo ""
