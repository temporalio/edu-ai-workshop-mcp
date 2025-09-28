# Making MCP Tools Durable Exercise #1

During this exercise, you will:

- TODO

Make your changes to the code in the `practice` subdirectory (look for TODO comments that will guide you to where you should make changes to the code). If you need a hint or want to verify your changes, look at the complete version in the `solution` subdirectory.

## Part A: 

1. We’ve already included an Activity named `convert_currency` in `activities.py`. This Activity converts your invoice’s currency to another currency, with USD as the default.
2. In `workflows.py`, add this Activity into your imports.

## Part E: 

10. Run the Temporal server with `temporal server start-dev`.
11. Run your Worker with `python worker.py`.
12. Copy this configuration to your Claude Desktop config file: `cp claude_desktop_config.json ~/Library/Application\ Support/Claude/`.
13. Restart Claude Desktop
14. Test your tool by prompting Claude Desktop for the weather from a city of your choice and a chart that visualizes the weather.


{
    "invoice_id": "INV-2024-EUR-001",
    "customer": "European Tech GmbH",
    "amount": 15000.00,
    "currency": "EUR",
    "description": "Software consulting services",
    "date": "2024-01-15",
    "convert_currency": {
      "amount": 15000.00,
      "from_currency": "EUR",
      "to_currency": "USD"
    },
    "items": [
      {
        "description": "Backend API Development",
        "amount": 10000.00,
        "currency": "EUR"
      },
      {
        "description": "Frontend UI Implementation",
        "amount": 5000.00,
        "currency": "EUR"
      }
    ]
  }