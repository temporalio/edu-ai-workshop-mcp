FROM mcr.microsoft.com/devcontainers/python:3.11

# Install Temporal CLI
RUN curl -sSf https://temporal.download/cli.sh | sh && \
    echo 'export PATH="$PATH:/home/vscode/.temporalio/bin"' >> /home/vscode/.bashrc

# Install desktop environment + Claude Desktop
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        fluxbox x11vnc novnc websockify xterm x11-utils dbus-x11 xvfb && \
    cd /tmp && \
    wget -q -O claude.deb \
        "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop-linux-x64-latest.deb" && \
    apt-get install -y --no-install-recommends ./claude.deb && \
    rm claude.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Go feature
RUN curl -fsSL https://go.dev/dl/go1.23.5.linux-amd64.tar.gz | tar -C /usr/local -xzf -
ENV PATH="/usr/local/go/bin:${PATH}"

# Switch to vscode user
USER vscode
WORKDIR /home/vscode

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/vscode/.local/bin:/home/vscode/.temporalio/bin:${PATH}"

# Pre-install Python dependencies (speeds up first run)
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev || true

WORKDIR /workspaces