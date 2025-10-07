## Creating your MCP Tool to query for status
from temporalio.client import Client
from fastmcp import FastMCP
import uuid
from typing import Dict

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
    """Start the InvoiceWorkflow with the given invoice JSON."""
    client = await get_temporal_client()
    handle = await client.start_workflow(
        "InvoiceWorkflow",
        invoice,
        id=f"invoice-{uuid.uuid4()}",
        task_queue="invoice-task-queue",
    )
    return {"workflow_id": handle.id, "run_id": handle.result_run_id}

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

@mcp.tool
async def approve_invoice(workflow_id: str, run_id: str) -> str:
    """Signal approval for the invoice workflow."""
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id=workflow_id, run_id=run_id)
    await handle.signal("ApproveInvoice")
    return "APPROVED"

@mcp.tool
async def reject_invoice(workflow_id: str, run_id: str) -> str:
    """Signal rejection for the invoice workflow."""
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id=workflow_id, run_id=run_id)
    await handle.signal("RejectInvoice")
    return "REJECTED"

@mcp.tool
async def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict[str, str]:
    """Convert a specific amount from one currency to another using the ConvertCurrencyWorkflow.
    
    Use this tool when the user wants to convert a currency amount (e.g., "convert 15000 EUR to USD")."""
    client = await get_temporal_client()
    handle = await client.start_workflow(
        "ConvertCurrencyWorkflow",
        args=[amount, from_currency, to_currency],
        id=f"convert-currency-{uuid.uuid4()}",
        task_queue="invoice-task-queue",
    )
    return {"workflow_id": handle.id, "run_id": handle.result_run_id}

@mcp.tool
async def get_conversion_amount(workflow_id: str, run_id: str) -> float | None:
    """Query the converted amount from a currency conversion workflow."""
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id=workflow_id, run_id=run_id)
    amount = await handle.query("GetConversionAmount")
    return amount

@mcp.tool
async def confirm_database_add(workflow_id: str) -> str:
    """Confirm that the converted amount has been added to the Dummy database.

    This simulates adding the converted amount to a Dummy database and signals
    the workflow to complete.
    """
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id=workflow_id)
    # Dummy print statement simulating database add
    print(f"${workflow_id} was added to the Dummy database")
    # Signal the workflow that the database add is confirmed
    await handle.signal("ConfirmDatabaseAdd")
    return f"Conversion for workflow {workflow_id}added to Dummy database"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="sse", host="0.0.0.0", port=5125)