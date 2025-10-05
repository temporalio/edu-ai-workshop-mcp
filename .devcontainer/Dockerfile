FROM mcr.microsoft.com/devcontainers/python:3.11

# Install Temporal CLI
RUN curl -sSf https://temporal.download/cli.sh | sh && \
    echo 'export PATH="$PATH:/home/vscode/.temporalio/bin"' >> /home/vscode/.bashrc

# Install desktop environment ONLY (no Claude Desktop yet)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        fluxbox x11vnc novnc websockify xterm x11-utils dbus-x11 xvfb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Go
RUN curl -fsSL https://go.dev/dl/go1.23.5.linux-amd64.tar.gz | tar -C /usr/local -xzf -
ENV PATH="/usr/local/go/bin:${PATH}"

USER vscode
WORKDIR /home/vscode

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/vscode/.local/bin:/home/vscode/.temporalio/bin:${PATH}"

WORKDIR /workspaces