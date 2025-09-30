# Making MCP Tools Durable Exercise #1

During this exercise, you will:

- Implement Temporal Signals to confirm downstream systems recorded the conversion.
- Build Temporal Queries to fetch the latest conversion amount from workflow state.
- Pause workflow progress with `workflow.wait_condition` so it waits on Signals or timeouts.
- Add durability to long-running workflows by exposing them through MCP tools and workers.

Make your changes to the code in the `practice` subdirectory (look for TODO comments that will guide you to where you should make changes to the code). If you need a hint or want to verify your changes, look at the complete version in the `solution` subdirectory.

## Part A: Set up Your `convert_currency` Activity

1. We’ve already included an Activity named `convert_currency` in `activities.py`. This Activity converts your invoice’s currency to another currency, with USD as the default.
2. In `workflows.py`, call your `convert_currency` Activity.
4. Pass in the arguments of `amount`, `from_currency`, `to_currency`.
5. Set your Start-to-Close Timeout to be 30 seconds.

## Part B: Create a Query to Get Conversion Amount

6. Now let's create a Query to get the conversion amount. In `workflows.py`, create a Query that gets the conversion amount and returns the value of `converted_amount` (already set for you).
7. At the end of the Workflow, return the value of the `converted_amount`.

## Part C: Create a Signal that Confirms Converseion Amount

7. We will now create a Signal that confirms that the conversion amount has been added to your database. In `workflows.py`, create a Signal that sets the value of `db_entry_confirmed` (already set for you) to `True`.
8. In this Workflow, we want to pause execution until either one of two conditions is met:
  a. `self.db_entry_confirmed` becomes `True`, or
  b. 5 days pass (whichever happens first).
To do this, we will use `workflow.wait_condition`. Please invoke this logic.
9. Save your Workflow file.

## Part D: Setting Up Your MCP Tools
10. In `mcp_servers/invoice.py` please add a tool in to invoke the `ConvertCurrencyWorkflow`. We will provide it here:

```python
@mcp.tool()
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
12. Create a tool which invokes the `GetConversionAmount` Query.
13. Save your `mcp_servers/invoice.py` file.

## Part E: Testing Your MCP Tools

14. Run the Temporal server with `temporal server start-dev`.
15. Run your Worker with `python worker.py` from the `practice` directory.
16. Copy this configuration to your Claude Desktop config file: `cp claude_desktop_config.json ~/Library/Application\ Support/Claude/`.
17. Restart Claude Desktop
18. Test your tool by prompting Claude Desktop for the following: 

`Can you convert this amount into USD:
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
}`
19. Look at the Web UI and confirm that your Workflow is running.
20. In Claude Desktop, complete the Workflow Execution by letting it know that you want to add this conversion to the database.
21. Test your Query by prompting Claude Desktop for the conversion amount.

## This is the end of the exercise.