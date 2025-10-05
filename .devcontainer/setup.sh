#!/bin/bash
set -e

echo "=== Workshop Setup (installing Jupyter) ==="
exec > >(tee -a /tmp/setup.log) 2>&1

export PATH="$HOME/.local/bin:$PATH"

# Just sync and install Jupyter (everything else is in the image)
cd /workspaces/edu-ai-workshop-mcp
uv sync
uv pip install ipykernel jupyter
uv run python -m ipykernel install --user --name='python3' --display-name='Python 3 (ipykernel)'

echo "Setup complete!"