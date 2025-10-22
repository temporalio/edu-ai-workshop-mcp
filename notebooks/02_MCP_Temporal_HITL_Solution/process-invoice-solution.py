from temporalio.client import Client
from fastmcp import FastMCP
from typing import Dict
import uuid

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
async def process_invoice(invoice: Dict) -> Dict[str, str]:
    """Process an invoice by starting the InvoiceWorkflow.
    Use this tool whenever the user asks to process or submit an invoice. 

    Args: invoice: Dictionary containing invoice_id, customer, and lines array with description, amount, and due_date
    Returns: Dictionary with workflow_id and run_id for tracking the invoice processing
     
    """
    client = await get_temporal_client()
    handle = await client.start_workflow(
        "InvoiceWorkflow",
        invoice,
        id=f"invoice-{uuid.uuid4()}",
        task_queue="invoice-task-queue",
    )
    return {"workflow_id": handle.id, "run_id": handle.result_run_id}