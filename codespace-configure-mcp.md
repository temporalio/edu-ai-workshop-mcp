# Configure Your MCP Server on Codespace with Claude Desktop

This guide helps you connect your MCP Server running in Codespaces to Claude Desktop running on your local machine.

## Architecture

- **Codespaces (Remote)**: Runs the MCP server
- **Local Machine**: Runs Claude Desktop + `mcp-remote` proxy

## Setup Steps

1. **Install mcp-remote**

   a. Make sure you already have [Node v20+](https://nodejs.org/en/download) installed on your machine. 
    - To check, run: `node --v`
    - Upgrade on [windows](https://nodesource.com/blog/Update-nodejs-versions-on-windows)
    - Upgrade on [Mac](https://nodesource.com/blog/update-Node.js-versions-on-MacOS)
   
   b. Over in Codespace, on the file explorer, on the left hand side you'll see `setup-mcp-remote.sh`. Right click, then click `Download` to save this file to your local machine.

   c. Open the terminal on your local machine and navigate to where you downloaded `setup-mcp-remote.sh`.

   d. Run `chmod +x setup-mcp-remote.sh`, then `./setup-mcp-remote.sh`.

   e. There will be two configurations, one for `claude_desktop_config.json` in Codespace and one for `claude_desktop_config.json` in Claude Desktop. Copy the JSON output for Codespace and paste it to `claude_desktop_config.json` on Codespace.

   f. Leave this terminal window open until we are done with the setup.

   _Disclaimer: You need [`mcp-remote`](https://www.npmjs.com/package/mcp-remote), a Node.js package which connects Claude Desktop to remote MCP servers via HTTP/SSE. Without it, Claude Desktop can only connect to MCP servers running locally. You need to install `mcp-remote` and you need to do so with Node.js 20+. This script will do this for you._

2. **Get your MCP Server URL**

   a. Over in Codespace, in a terminal window, run `./get-mcp-url.sh` to get your MCP Server URL.

   b. Copy the URL output (e.g., `https://xxx-5125.app.github.dev/sse`) and paste it to `claude_desktop_config.json` where it says `<YOUR_CODESPACES_URL_HERE>`.

   c. Your final JSON on Codespace should look something like this:

```json
{
    "mcpServers": {
        "weather": {
            "command": "/opt/homebrew/bin/mcp-remote",
            "args": [
                "https://refactored-umbrella-r4gp54pg4g6g2pvvw-5125.app.github.dev/sse"
            ]
        }
    }
}
```

3. **Start the MCP Server on a terminal window in Codespace**

   a. In a new terminal window in Codespace, run `uv run python mcp_servers/weather.py`. Close any popup windows that may appear.

    _Note: To create more work terminals for this workshop, use the drop-down arrow on the right side of the screen, navigate to "Split Terminal"._
    ![9 — Split Terminal](https://i.postimg.cc/tC46G9Bh/9-split-terminal.png)

   b. Leave this sever running.

4. **Configure Claude Desktop**

   a. Make sure [Claude Desktop](https://claude.ai/download) is installed on your local machine.

   b. Open Claude Desktop.

   c. Menu bar → `Claude` → `Settings` → `Developer` → `Edit Config`

   d. Right-click `claude_desktop_config.json` → `Open With` → `Text Edit` (or `Notepad` on Windows)

   e. Copy the JSON output for Claude Desktop from step 1 and paste it in the `Text Edit`. Copy the MCP Server URL, which was the configuration output from step 2 (e.g., `https://xxx-5125.app.github.dev/sse`).

   f. In `claude_desktop_config.json` on Claude Desktop, and replace `<YOUR_CODESPACES_URL_HERE>` with the MCP Server URL. Your final config for Claude Desktop should look like:

```json
{
    "mcpServers": {
        "weather": {
            "command": "/opt/homebrew/bin/node",
            "args": [
                "/opt/homebrew/lib/node_modules/mcp-remote/dist/proxy.js",
                "https://refactored-umbrella-r4gp54pg4g6g2pvvw-5125.app.github.dev/sse"
            ]
        }
    }
}
```

5. **Restart Claude Desktop**

6. When you open Claude Desktop, click on the icon to the right of the plus sign button. You should now see your configured MCP server (e.g., weather) on your Claude Desktop and the blue toggle should be switched on.

![Configured Claude Desktop](https://i.postimg.cc/8kWjM9Sm/claude-desktop-mcp-server-configured.png "Configured Claude Desktop")

Troubleshooting Note: If you see the MCP server configured, but the blue toggle is not switched on, just try restarting Claude Desktop again.

---
**Troubleshooting Notes**:
- If your Claude desktop is stuck and not loading, even on a force quit, this may be because of an incorrect configuration. In this case, search for `claude_desktop_config.json` from your machine instead and edit the file from there instead of from Claude Desktop.
- Make sure Port 5125 visibility is set to Public. This should be already switched on automatically but if it's not connecting, make sure to check this.