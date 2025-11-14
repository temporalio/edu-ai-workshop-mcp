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
async def process_invoice(
    invoice_id: str,
    customer: str, 
    item_description: str,
    amount: float,
    due_date: str
) -> Dict[str, str]:
    """
    Process an invoice by starting the InvoiceWorkflow.
    Use this tool whenever the user asks to process or submit an invoice.
    
    Args:
    invoice_id: Invoice ID (e.g., "INV-100")
    customer: Customer name (e.g., "ACME Corp")
    item_description: Description of the item (e.g., "Widget A")
    amount: Amount in dollars (e.g., 100)
    due_date: Due date in YYYY-MM-DD format (e.g., "2025-06-30")
        
    Returns: Dictionary with workflow_id and run_id
    """

    invoice = {
        "invoice_id": invoice_id,
        "customer": customer,
        "lines": [
            {
                "description": item_description,
                "amount": amount,
                "due_date": due_date
            }
        ]
    }

    client = await get_temporal_client()
    handle = await client.start_workflow(
        "InvoiceWorkflow",
        invoice,
        id=f"invoice-{uuid.uuid4()}",
        task_queue="invoice-task-queue",
    )
    return {"workflow_id": handle.id, "run_id": handle.result_run_id}

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="sse", host="0.0.0.0", port=5125)