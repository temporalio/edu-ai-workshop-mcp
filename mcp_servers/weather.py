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
    # Initialize and run the server
    mcp.run(transport="sse", host="0.0.0.0", port=5125)

# Note: The SSE transport for MCP is deprecated, officially replaced by the HTTP Protocol.
# We will replace this protocol at a later time.