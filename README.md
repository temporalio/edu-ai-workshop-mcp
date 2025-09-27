# AI Agent Workshop with Temporal

This repository contains a hands-on workshop demonstrating how to build durable MCP tools.
## Workshop Overview

## Repository Structure

```
├── notebooks/          # Interactive Jupyter notebooks for the workshop
│   └── exercises/      # Hands-on exercises
```

## Prerequisites

- Python 3.13+
- OpenAI API key (or other LLM provider API key)
- Basic familiarity with Python and async programming

## Installation

### 1. Install Python 3.13 with uv

This project uses `uv` for Python version and package management:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python 3.13
uv python install 3.13

# Verify installation
uv python list
```

#### 2. Setup

1. Create a virtual environment: `python -m venv env`
2. Activate the environment:
   - Mac: `source env/bin/activate`
   - Windows: `env\Scripts\activate`
3. Install dependencies from `pyproject.toml` directory: `uv pip install -r pyproject.toml`

## Running the Workshop

### Option 1: Google Colab

You can use [Google Colab](https://colab.research.google.com/) and run the workshop from the files in this [Google Drive]().

1. Ensure you are signed in to a Google account.
2. Open the notebook, go to **File** and click **Save a copy in Drive** to save the notebook to your Google Drive.
3. Follow the notebook instructions step by step. Do this for every content and exercise.

### Option 2: Interactive Notebooks

For the complete workshop experience with explanations:

1. Start Jupyter Lab:
   ```bash
   uv run --with jupyter jupyter lab
   ```

2. Navigate to `notebooks/content/` and open `01_An_AI_Agent.ipynb`

3. Follow the notebook instructions step by step

### Option 3: Standalone Code Examples

For running the code examples directly, follow the README in the `src` directory.

#### Module 1: Basic AI Agent

This demonstrates a simple agent that:
- Prompts for a research topic
- Calls an LLM for research
- Generates a PDF report
- Shows the limitations of non-durable execution

#### Module 2: Durable Execution with Temporal

- Fault-tolerant execution that survives process crashes
- Automatic retries with exponential backoff
- State persistence across worker restarts
- Monitoring via Temporal Web UI at http://localhost:8080

#### Module 3: Human-in-the-Loop

- Pausing workflows for human decision-making
- Using Temporal Signals for real-time communication
- Allowing humans to approve or modify AI-generated content

## Development Commands

The project uses `just` for development automation:

```bash
just check          # Run all checks (lint, format-check, typecheck)
just fix            # Auto-fix linting and formatting issues  
just lint           # Run ruff linter with fixes
just format         # Format code with ruff
just typecheck      # Run mypy type checking
just clean          # Remove Python cache files
```

- Check the Temporal documentation: https://docs.temporal.io/

## Contributing

This workshop is designed for educational purposes. Feel free to:
- Submit issues for bugs or unclear instructions
- Propose improvements to the examples
- Share your own AI agent implementations

## License

[Include appropriate license information]