from typing import Any
from temporalio import activity
import httpx

USER_AGENT = "weather-app/1.0"

@activity.defn # Implement the Activity as a function decorated with the `@activity.defn` decorator.
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:

        response = await client.get(url, headers=headers, timeout=5.0)
        response.raise_for_status()
        return response.json()
