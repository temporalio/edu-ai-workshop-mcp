# Note: MCP servers cannot be run directly in Jupyter notebooks because
# MCP servers need to run as separate processes that communicate with stdio protocol
# Therefore, we also have this code in a separate Python file that can be run
# as a standalone MCP server (mcp_servers/weather.py).

from temporalio.client import Client
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Temporal client setup (do this once, then reuse)
temporal_client = None

async def get_temporal_client():
    global temporal_client
    if not temporal_client:
        temporal_client = await Client.connect("localhost:7233")
    return temporal_client

@mcp.tool
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # The business logic has been moved into the temporal workflow, the mcp tool kicks off the workflow
    client = await get_temporal_client()
    handle = await client.start_workflow(
        workflow="GetForecast",
        args=[latitude, longitude],
        id=f"forecast-{latitude}-{longitude}",
        task_queue="weather-task-queue",
    )
    return await handle.result()

    if __name__ == "__main__":
        mcp.run(transport='stdio')
