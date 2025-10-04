#!/bin/bash
set -e

echo "=== Fast Workshop Setup (Python only) ==="
exec > >(tee -a /tmp/setup.log) 2>&1

# Python setup
echo "Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

echo "Installing workshop dependencies..."
uv sync

echo "Setting up Jupyter kernel..."
uv pip install ipykernel jupyter
uv run python -m ipykernel install --user --name='python3' --display-name='Python 3 (ipykernel)'

echo "Claude Desktop installing in background..."