from typing import Any
import httpx
from temporalio import activity
from temporalio.exceptions import ApplicationError

USER_AGENT = "weather-app/1.0"

@activity.defn
async def make_nws_request_buggy(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    raise ApplicationError( # Remove the error by commenting it out or deleting it
        "Simulated timeout: Weather service temporarily unavailable"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=5.0)
        response.raise_for_status()
        return response.json()