# Step-by-Step Tutorial: Testing Your MCP Tools with Streamlit

Follow these steps to test the Streamlit MCP client interface with your Temporal workflows.

---

## Prerequisites

Make sure you have:
- GitHub Codespace running
- OpenAI API key ready

---

## Step 1: Set Up Environment Variables

Run the interactive setup script to create your `.env` file:

```bash
chmod +x setup-env.sh
./setup-env.sh
```

This will prompt you for:
1. Your OpenAI API key
2. Your preferred model (gpt-4o, gpt-4o-mini, etc.)
3. Auto-generates your Codespace MCP Server URL

---

## Step 2: Start Temporal Server

In terminal 1, start the Temporal server:

```bash
temporal server start-dev
```

**What to expect:**
- Server logs will appear
- Leave this terminal running
- Access Web UI at the forwarded port 8233

---

## Step 3: Start the Worker

In terminal 2, navigate to the solution directory and start the worker:

```bash
cd exercises/01_Making_MCP_Tools_Durable/solution
python worker.py
```

**What to expect:**
- You'll see: "Worker started. Listening for workflows..."
- Leave this terminal running

---

## Step 4: Start the MCP Server

In terminal 3, start the MCP server:

```bash
uv run mcp_servers/weather.py
```

**What to expect:**
- Server starts on port 5125
- You'll see SSE server logs
- Leave this terminal running

---

## Step 5: Start Streamlit Interface

In terminal 4, load your environment variables and start Streamlit:

```bash
source load-env.sh
uv run streamlit run mcp_chat_interface.py
```

**What to expect:**
- Streamlit will start and provide a URL
- In Codespace, click the popup or go to Ports tab and click the globe icon next to port 8501
- Browser will open with the MCP Chat Interface

---

## Step 6: Configure and Use the Interface

### In the Streamlit Interface:

1. **Check the sidebar (left side):**
   - Your OpenAI API key should be pre-filled (as `********`)
   - Model should be set (e.g., gpt-4o)
   - MCP Server URL should be filled with your Codespace URL
   - You should see "Loaded 1 tools" in green
   - Under "Available Tools", you should see `get_forecast`

2. **If you don't see "Loaded 1 tools":**
   - Click the "Load MCP Tools" button
   - Wait a moment for it to connect

3. **Start chatting:**
   - At the bottom of the page, you'll see a chat input box
   - Type: "What's the weather in San Francisco?"
   - Press Enter

4. **Watch the magic happen:**
   - GPT receives your message
   - GPT decides to use the get_forecast tool
   - Tool call is displayed in a blue info box
   - MCP tool triggers a Temporal workflow
   - Results are returned and displayed
   - GPT responds with a natural language answer

5. **Check Temporal Web UI:**
   - Go to your Ports tab, open port 8233
   - You'll see a workflow execution for your weather request
   - Click on it to see the event history

---

## Step 7: Try More Queries

**Weather queries to try:**
- "Get weather forecast for New York" (latitude: 40.7128, longitude: -74.0060)
- "What's the forecast for Seattle?" (latitude: 47.6062, longitude: -122.3321)
- "Tell me the weather in Tokyo" (latitude: 35.6762, longitude: 139.6503)

Each query will trigger a new Temporal workflow that you can monitor in the Web UI!

---

## Troubleshooting

### "Please enter your API Key in the sidebar"
**Solution:**
- Make sure you ran `source load-env.sh` before starting Streamlit
- Or manually enter your API key in the sidebar

### "No tools found" or "Failed to connect to MCP server"
**Solution:**
- Check that the MCP server is running (`uv run mcp_servers/weather.py`)
- Verify the URL in the sidebar matches your Codespace URL
- Click "Load MCP Tools" again

### "Connection refused"
**Solution:**
- Make sure all three services are running:
  - Temporal server (port 7233)
  - Worker (python worker.py)
  - MCP server (port 5125)

### Chat input doesn't appear
**Solution:**
- Enter your API key in the sidebar first
- Wait for "Loaded 1 tools" confirmation
- The chat input will appear at the bottom

---

## Advanced: Test with Invoice Server

Want to try the invoice processing with human-in-the-loop? Follow these steps:

### Stop the weather services:
```bash
# Terminal 2 (worker) - Press Ctrl+C
# Terminal 3 (MCP server) - Press Ctrl+C
```

### Start invoice services:

**Terminal 2 (new worker):**
```bash
cd exercises/02_MCP_Temporal_HITL/solution
python worker.py
```

**Terminal 3 (new MCP server):**
```bash
uv run exercises/02_MCP_Temporal_HITL/solution/mcp_servers/invoice.py
```

### In Streamlit:
1. Click "Load MCP Tools" again
2. You should now see 4 tools:
   - process_invoice
   - invoice_status
   - approve_invoice
   - reject_invoice

3. Try processing an invoice:
```
Process this invoice:
{
  "invoice_id": "INV-100",
  "customer": "ACME Corp",
  "lines": [
    {"description": "Widget A", "amount": 100, "due_date": "2024-06-30T00:00:00Z"},
    {"description": "Widget B", "amount": 200, "due_date": "2024-07-05T00:00:00Z"}
  ]
}
```

4. Check the status: "What's the status of this invoice?"

5. Go to Temporal Web UI - the workflow is RUNNING and waiting for approval

6. **Test durability**: Kill the MCP server (Ctrl+C), check Web UI - workflow still running!

7. Restart MCP server, then approve: "Approve this invoice"

8. Watch the workflow complete in Temporal Web UI!

---

## Summary

You've successfully:
- Set up a complete MCP + Temporal + OpenAI stack
- Created durable MCP tools backed by Temporal workflows
- Used a chat interface to interact with your tools
- Monitored workflow executions in real-time
- Tested the durability and persistence of Temporal

This is the foundation for building robust, production-ready agentic systems!
