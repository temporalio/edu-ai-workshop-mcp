# Making MCP Tools Durable Exercise #1

In this exercise, you'll add another MCP tool which helps convert currency for you if your invoice is in a different currency. You'll also create a Signal that simulates adding the converted amount to a dummy database and signals the workflow to complete. You'll also create a query that queries for the converted amount from a currency conversion workflow

During this exercise, you will:

- Implement a Temporal Signal to send external input to your running Workflow Execution
- Build a Temporal Query to fetch the data from your Workflow state
- Pause Workflow progress so it waits on Signals or timeouts
- Add durability to long-running workflows by exposing them through MCP tools

Make your changes to the code in the `practice` subdirectory (look for TODO comments that will guide you to where you should make changes to the code). If you need a hint or want to verify your changes, look at the complete version in the `solution` subdirectory.

## Part A: Set up Your `convert_currency` Activity

1. We’ve already included an Activity named `convert_currency` in `activities.py`. This Activity converts your invoice’s currency to another currency, with USD as the default.
2. In `workflows.py`, call your `convert_currency` Activity.
4. Pass in the arguments of `amount`, `from_currency`, `to_currency`.
5. Set your Start-to-Close Timeout to be 30 seconds.

## Part B: Create a Query to Get Conversion Amount

6. Now let's create a Query, `GetConversionAmount`, to get the conversion amount. In `workflows.py`, create a Query that gets the conversion amount and returns the current value of `converted_amount` (already set for you).
7. At the end of the Workflow, return the value of the `converted_amount`.

## Part C: Create a Signal that Confirms Converseion Amount

7. We will now create a Signal, `ConfirmDatabaseAdd`, that confirms that the conversion amount has been added to your database. In `workflows.py`, create a Signal that sets the value of `db_entry_confirmed` (already set for you) to `True`.
8. In this Workflow, we want to pause execution until either one of two conditions is met:
  a. `self.db_entry_confirmed` becomes `True`, or
  b. 5 days pass (whichever happens first).
To do this, we will use `workflow.wait_condition`. Please invoke this logic.
9. Save your Workflow file.

## Part D: Setting Up Your MCP Tools
10. In `mcp_servers/invoice.py` (at root of directory) please add a tool in to invoke the `ConvertCurrencyWorkflow`. We will provide it here:

```python
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
```

11. Next, create a tool which invokes the `ConfirmDatabaseAdd` Signal.
  - Use this provided comment that describes what the tool does so that the tool can present its capabilities to MCP Client. 
  ```
    """Signal the workflow to add the converted amount to the dummy database and complete.
      
    Use this tool when the user says to confirm, add, or store the conversion to the database.
    This will signal the workflow to proceed with the simulated database add.
    
    Args:
        workflow_id: The workflow ID from convert_currency
        run_id: The run ID from convert_currency
    
    Returns:
        Confirmation message
    """
    ```
12. Create a tool which invokes the `GetConversionAmount` Query.
  - Use this provided comment that describes what the tool does so that the tool can present its capabilities to the MCP Client. 
  """Query the converted amount from a currency conversion workflow."""
  - Our solution is in our solution is in `/solution/mcp_servers/invoice.py`
13. Save your `mcp_servers/invoice.py` file.

## Part E: Testing Your MCP Tools

10. Run your Worker with `uv run worker.py` from the `practice` directory in a new terminal.
11. To register a new tool, restart the MCP server in Codespaces. Do this by going to the terminal window where you're running `uv run mcp_servers/invoice.py`, stop it with `Ctrl+C`, then run it again.
12. Go to the MCP Client interface and click `Load More Tools`. You should now see seven available tools: `process_invoice`, `invoice_status`, `approve_invoice`, `reject_invoice`, `convert_currency`, `get_conversion_amount`, `confirm_database_add`.
13. Clear the chat with the `Clear Chat` button on the bottom left. In the chat interface, ask something like: `Can you convert this amount from EUR to USD? The current exchange rate is 1.16 USD per EUR:
{
  "invoice_id": "INV-2024-EUR-001",
  "customer": "European Tech GmbH",
  "total_amount": 15000.00,
  "currency": "EUR",
  "description": "Software consulting services",
  "date": "2024-01-15",
  "lines": [
    {
      "item_id": "line-1",
      "description": "Backend API Development",
      "amount": 10000.00,
      "currency": "EUR"
    },
    {
      "item_id": "line-2", 
      "description": "Frontend UI Implementation",
      "amount": 5000.00,
      "currency": "EUR"
    }
  ]
}`. The `convert_currency` tool will be called.
14. Look at the Web UI and confirm that your Workflow is running.
15. In your MCP Client interface, complete the Workflow Execution by: "Confirm that the converted amount has been added to the Dummy database and complete workflow execution."
16. Test your Query by prompting the MCP Client Interface for the conversion amount.

## This is the end of the exercise.