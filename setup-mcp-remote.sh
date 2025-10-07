#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "========================================"
echo "MCP Remote Setup Script"
echo "========================================"

# Function to check if Node.js version is 20 or higher
check_node_version() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$NODE_VERSION" -ge 20 ]; then
            echo -e "${GREEN}✓ Node.js $NODE_VERSION is installed${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠ Node.js $NODE_VERSION is installed but version 20+ is required${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠ Node.js is not installed${NC}"
        return 1
    fi
}

# Function to install Node.js using nvm
install_nodejs() {
    echo -e "${YELLOW}Installing Node.js 20 using nvm...${NC}"

    # Install nvm if not present
    if ! command -v nvm &> /dev/null && [ ! -s "$HOME/.nvm/nvm.sh" ]; then
        echo "Installing nvm..."
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

        # Load nvm
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    else
        # Load nvm if it exists
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    fi

    # Install Node.js 20
    nvm install 20
    nvm use 20
    nvm alias default 20

    echo -e "${GREEN}✓ Node.js 20 installed${NC}"
}

# Function to install mcp-remote
install_mcp_remote() {
    echo -e "${YELLOW}Installing mcp-remote...${NC}"
    npm install -g mcp-remote
    echo -e "${GREEN}✓ mcp-remote installed${NC}"
}

# Main execution
echo ""
echo "Step 1: Checking Node.js..."
if ! check_node_version; then
    install_nodejs
fi

# Reload environment to ensure node is in PATH
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

echo ""
echo "Step 2: Installing mcp-remote..."
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
