from typing import Any
from temporalio import activity
import httpx

USER_AGENT = "weather-app/1.0"

@activity.defn
async def make_nws_request_buggy(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=5.0)
        response.raise_for_status()
        return response.json()