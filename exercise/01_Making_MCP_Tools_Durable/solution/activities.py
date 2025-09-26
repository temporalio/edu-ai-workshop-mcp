from typing import Any, Dict
from temporalio import activity
import httpx
import json
import urllib.parse

USER_AGENT = "weather-app/1.0"

@activity.defn
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


@activity.defn
async def generate_weather_chart(
    weather_data: Dict[str, Any],
    include_precipitation: bool = False,
    num_days: int = 5
) -> str:
    """Generate a weather chart from NWS data using QuickChart API.

    Args:
        weather_data: Weather data from NWS API
        include_precipitation: If True, includes precipitation data
        num_days: Number of days to show (max 7)

    Returns:
        URL of the generated chart image
    """
    # Extract periods
    periods = weather_data.get("properties", {}).get("periods", [])[:num_days * 2]
    if not periods:
        raise ValueError("No forecast periods found in weather data")

    # Prepare data safely
    labels = []
    temps = []

    for p in periods:
        name = str(p.get("name", ""))
        if len(name) > 15:
            name = name[:12] + "..."
        labels.append(name)
        temps.append(int(p.get("temperature", 0)))

    # Simple chart config
    chart_config = {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Temperature",
                "data": temps,
                "borderColor": "red",
                "fill": False
            }]
        },
        "options": {
            "title": {
                "display": True,
                "text": "Weather Forecast"
            }
        }
    }

    # Add precipitation if requested
    if include_precipitation:
        precip = []
        for p in periods:
            val = p.get("probabilityOfPrecipitation", {}).get("value", 0)
            precip.append(int(val) if val else 0)

        chart_config["data"]["datasets"][0]["yAxisID"] = "y-axis-1"
        chart_config["data"]["datasets"].append({
            "label": "Precip %",
            "data": precip,
            "borderColor": "blue",
            "yAxisID": "y-axis-2",
            "fill": False
        })

        chart_config["options"]["scales"] = {
            "yAxes": [
                {"id": "y-axis-1", "type": "linear", "position": "left"},
                {"id": "y-axis-2", "type": "linear", "position": "right", "ticks": {"max": 100, "min": 0}}
            ]
        }

    # Generate URL with proper encoding
    chart_json = json.dumps(chart_config)
    params = {"c": chart_json, "width": 800, "height": 400}
    encoded = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    return f"https://quickchart.io/chart?{encoded}"