# Making MCP Tools Durable Exercise #1

In this exercise, you'll create an additional tool for Claude Desktop to be able to use: creating a chart to plot the temperature in a place over the span of five days. After having Claude Desktop give you the weather forecast, you'll then generate a chart as well.

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
9. Use this provided comment that describes what the tool does so that the tool can present its capabilities to Claude Desktop. Save your file.
Provided comment:

"""Generate a weather chart visualization for a location using Temporal workflow.

    This tool fetches weather data and creates a chart showing temperature trends,
    and optionally precipitation chances over the forecast period.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        include_precipitation: If True, generates an advanced chart with both temperature
                               and precipitation data. If False, generates a simple
                               temperature-only chart.

    Returns:
        A dictionary containing:
        - success: Whether the chart was generated successfully
        - location: The city and state of the location
        - chart_url: URL to the generated chart image
        - summary: Brief weather summary for the next few periods
        - message: Status message
        - error: Error message if unsuccessful
    """

## Part E: Test your MCP tool

10. Run your Worker with `uv run worker.py` from the `practice` directory in a new terminal.
11. To register a new tool, restart the MCP server in Codespaces. Do this by going to the terminal window where you're running `uv run mcp_servers/weather.py`, stop it with `Ctrl+C`, then run it again.
12. Go to the MCP Client interface and click `Load More Tools`. You should now see two available tools: `get_forecast` and `get_weather_chart`.
13. Test your tool by prompting Claude Desktop first for the weather forecast from a city of your choice. OpenAI will decide to use the `get_forecast` tool.
14. Then ask it to 'make me a chart to visualize the weather data'. OpenAI will decide to use the `get_weather_chart` tool.
15. Allow it to use the `Get Weather Chart` tool.

## This is the end of the exercise.