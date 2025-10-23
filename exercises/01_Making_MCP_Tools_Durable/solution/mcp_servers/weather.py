from temporalio.client import Client
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Temporal client setup (do this once, then reuse)
temporal_client = None

async def get_temporal_client():
    """Get or create a Temporal client connection."""
    global temporal_client
    if not temporal_client:
        temporal_client = await Client.connect("localhost:7233")
    return temporal_client

@mcp.tool
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location using Temporal workflow. Use this for any weather-related requests. 

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location

    Returns:
        Weather forecast for the specified location
    """
    client = await get_temporal_client()
    handle = await client.start_workflow(
        workflow="GetForecast",
        args=[latitude, longitude],
        id=f"forecast-{latitude}-{longitude}",
        task_queue="weather-task-queue",
    )
    return await handle.result()

@mcp.tool
async def get_weather_chart(
    latitude: float,
    longitude: float,
    include_precipitation: bool = False
) -> dict:
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
    client = await get_temporal_client()
    handle = await client.start_workflow(
        workflow="GetWeatherChart",
        args=[latitude, longitude, include_precipitation],
        id=f"weather-chart-{latitude}-{longitude}",
        task_queue="weather-task-queue",
    )
    return await handle.result()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="sse", host="0.0.0.0", port=5125)