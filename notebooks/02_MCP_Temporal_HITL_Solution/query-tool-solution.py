from temporalio.client import Client
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("invoice")

# Temporal client setup (do this once, then reuse)
temporal_client = None

async def get_temporal_client():
    """Get or create a Temporal client connection."""
    global temporal_client
    if not temporal_client:
        temporal_client = await Client.connect("localhost:7233")
    return temporal_client

@mcp.tool
async def invoice_status(workflow_id: str, run_id: str) -> str:
    """Return current status of the workflow."""
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id=workflow_id, run_id=run_id)
    desc = await handle.describe()
    status = await handle.query("GetInvoiceStatus")
    return (
        f"Invoice with ID {workflow_id} is currently {status}. "
        f"Workflow status: {desc.status.name}"
    )