#!/bin/bash
# Setup and load environment variables
# First run: Creates .env file with your configuration
# Subsequent runs: Loads existing .env file

# Check if .env already exists
if [ -f .env ]; then
    echo "=========================================="
    echo "  Loading Existing Configuration"
    echo "=========================================="
    echo ""

    # Load variables from .env file
    set -a
    source .env
    set +a

    echo "✓ Environment variables loaded from .env"
    echo ""
    echo "Current configuration:"
    echo "  LLM_MODEL: $LLM_MODEL"
    echo "  MCP_SERVER_URL: $MCP_SERVER_URL"
    echo "  LLM_API_KEY: ${LLM_API_KEY:0:8}..."
    echo ""
    echo "To reconfigure, delete .env and run this script again."
    echo ""

else
    # First time setup
    set -e

    echo "=========================================="
    echo "  MCP Workshop Environment Setup"
    echo "=========================================="
    echo ""

    # Generate Codespace MCP Server URL
    MCP_URL="https://$(echo $CODESPACE_NAME)-5125.app.github.dev/sse"
    echo "MCP Server URL: $MCP_URL"
    echo ""

    # Prompt for OpenAI API Key
    echo "Enter your OpenAI API Key (paste then hit enter):"
    read -s LLM_API_KEY
    echo ""

    if [ -z "$LLM_API_KEY" ]; then
        echo "Error: API Key cannot be empty"
        return 1 2>/dev/null || exit 1
    fi

    # Prompt for model selection
    echo "Select your OpenAI model (type the number then hit enter):"
    echo "1) gpt-4o (recommended)"
    echo "2) gpt-4o-mini (cheaper, faster)"
    echo "3) gpt-4-turbo"
    read -p "Enter choice [1-3]: " model_choice

    case $model_choice in
        1)
            LLM_MODEL="gpt-4o"
            ;;
        2)
            LLM_MODEL="gpt-4o-mini"
            ;;
        3)
            LLM_MODEL="gpt-4-turbo"
            ;;
        *)
            echo "Invalid choice. Using default: gpt-4o"
            LLM_MODEL="gpt-4o"
            ;;
    esac

    # Create .env file
    echo ""
    echo "Creating .env file..."
    cat > .env << EOF
# OpenAI Configuration
LLM_API_KEY="$LLM_API_KEY"
LLM_MODEL="$LLM_MODEL"

# MCP Server Configuration
MCP_SERVER_URL="$MCP_URL"
EOF

    # Make sure .env is in .gitignore
    if [ ! -f .gitignore ]; then
        echo ".env" > .gitignore
        echo "Created .gitignore with .env"
    elif ! grep -q "^\.env$" .gitignore; then
        echo ".env" >> .gitignore
        echo "Added .env to .gitignore"
    fi

    # Load the newly created .env
    set -a
    source .env
    set +a

    echo ""
    echo "=========================================="
    echo "  Configuration Summary"
    echo "=========================================="
    echo "Model: $LLM_MODEL"
    echo "MCP Server URL: $MCP_SERVER_URL"
    echo "API Key: ${LLM_API_KEY:0:8}..."
    echo ""
    echo "✓ .env file created successfully!"
    echo "✓ Variables exported to current shell"
    echo ""
fi

echo "=========================================="
echo "  Ready to Start!"
echo "=========================================="
echo ""
echo "Start Streamlit now:"
echo "  uv run streamlit run mcp_client_interface.py"
echo ""
echo "=========================================="
