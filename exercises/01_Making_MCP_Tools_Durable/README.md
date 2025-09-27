# Making MCP Tools Durable Exercise #1

During this exercise, you will:

- Build durability and persistence to your MCP tools with Temporal Workflows
- Test the integration between Claude Desktop, MCP servers, and Temporal workflows

Make your changes to the code in the `practice` subdirectory (look for TODO comments that will guide you to where you should make changes to the code). If you need a hint or want to verify your changes, look at the complete version in the `solution` subdirectory.

## Part A: Finalize your `generate_weather_chart` Activity

1. We’ve already provided you with an Activity called `generate_weather_chart` in `activities.py`. This Activity creates a chart that visualizes the weather, using data retrieved from the `make_nws_request` Activity. Add the `activity.defn` decorator.
2. In the `chart_config`, add a title for your chart. Save your Activities file.

## Part B: Call your `generate_weather_chart` Activity from your Workflow

3. In `workflows.py`, you will now call your `generate_weather_chart` Activity in your `GetWeatherChart` Workflow. When you get the forecast grid endpoint, call your `make_nws_request` Activity, pass in your `points_url`, and set your Schedule-To-Close Timeout to be 40 seconds.
4. After you get your forecast data, call your `generate_weather_chart` Activity.
5. Add your own success message that is returned by the Workflow. Save your file.

## Part C: Register your Activities and Workflows on your Worker

6. In `worker.py`, import your Activities.
7. Register your Activities and Workflows to the Worker. Save your file.

## Part D: Create your MCP Tool that generates your weather chart

8. In `mcp_servers/weather.py` (at the root of this directory), create a `get_weather_chart` tool that calls your `GetWeatherChart` Workflow. 
9. Use the provided comment that describes what the tool does so that the tool can present its capabilities to Claude Desktop. Save your file.

## Part E: Test your MCP tool

10. Run the Temporal server with `temporal server start-dev`.
11. Run your Worker with `python worker.py`.
12. Copy this configuration to your Claude Desktop config file: `cp claude_desktop_config.json ~/Library/Application\ Support/Claude/`.
13. Restart Claude Desktop
14. Test your tool by prompting Claude Desktop for the weather from a city of your choice and a chart that visualizes the weather.