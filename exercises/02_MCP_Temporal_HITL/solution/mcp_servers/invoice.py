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

  @mcp.tool()
  async def process_invoice(invoice: Dict) -> Dict[str, str]:
      """Start the InvoiceWorkflow with the given invoice JSON."""
      client = await get_temporal_client()  # Fixed: was _client()
      handle = await client.start_workflow(
          "InvoiceWorkflow",
          invoice,
          id=f"invoice-{uuid.uuid4()}",
          task_queue="invoice-task-queue",
      )
      return {"workflow_id": handle.id, "run_id": handle.result_run_id}

@mcp.tool()
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

@mcp.tool()
async def approve_invoice(workflow_id: str, run_id: str) -> str:
    """Signal approval for the invoice workflow."""
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id=workflow_id, run_id=run_id)
    await handle.signal("ApproveInvoice")
    return "APPROVED"

@mcp.tool()
async def reject_invoice(workflow_id: str, run_id: str) -> str:
    """Signal rejection for the invoice workflow."""
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id=workflow_id, run_id=run_id)
    await handle.signal("RejectInvoice")
    return "REJECTED"

@mcp.tool()
async def process_invoice_with_currency_conversion(
    invoice: Dict, convert_currency_params: Dict = None
) -> Dict[str, str]:
    """Start the InvoiceWorkflow with currency conversion.

    Args:
        invoice: The invoice JSON data (can include convert_currency directly)
        convert_currency_params: Optional dict with:
            - amount: Amount to convert (defaults to invoice total_amount)
            - from_currency: Source currency code (default: EUR)
            - to_currency: Target currency code (default: USD)
    """
    # If convert_currency_params provided separately, use it
    if convert_currency_params:
        invoice["convert_currency"] = convert_currency_params
    # Otherwise check if invoice already has currency conversion info
    elif "currency" in invoice and invoice["currency"] != "USD":
        # Auto-create conversion params from invoice data
        invoice["convert_currency"] = {
            "amount": invoice.get("amount", 0),
            "from_currency": invoice.get("currency", "EUR"),
            "to_currency": "USD"
        }

    client = await get_temporal_client()
    handle = await client.start_workflow(
        "InvoiceWorkflow",
        invoice,
        id=f"invoice-{uuid.uuid4()}",
        task_queue="invoice-task-queue",
    )
    return {"workflow_id": handle.id, "run_id": handle.result_run_id}
