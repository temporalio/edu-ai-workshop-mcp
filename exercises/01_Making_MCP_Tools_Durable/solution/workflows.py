from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
import json
import asyncio

retry_policy = RetryPolicy(
    maximum_attempts=0,  # Infinite retries
    initial_interval=timedelta(seconds=2),
    maximum_interval=timedelta(minutes=1),
    backoff_coefficient=1.0,
)

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Import activities with sandbox passthrough
with workflow.unsafe.imports_passed_through():
    from activities import make_nws_request, generate_weather_chart

@workflow.defn
class GetForecast:
    @workflow.run
    async def get_forecast(self, latitude: float, longitude: float) -> str:
        """Get weather forecast for a location.

        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
        """
        # First get the forecast grid endpoint
        points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
        points_data = await workflow.execute_activity(
            make_nws_request,
            points_url,
            schedule_to_close_timeout=timedelta(seconds=40),
            retry_policy=retry_policy,
        )

        if not points_data:
            return "Unable to fetch forecast data for this location."

        await workflow.sleep(10)

        # Get the forecast URL from the points response
        forecast_url = points_data["properties"]["forecast"]
        forecast_data = await workflow.execute_activity(
            make_nws_request,
            forecast_url,
            schedule_to_close_timeout=timedelta(seconds=40),
            retry_policy=retry_policy,
        )
        if not forecast_data:
            return "Unable to fetch detailed forecast."

        # Format the periods into a readable forecast
        periods = forecast_data["properties"]["periods"]
        forecasts = []
        for period in periods[:5]:  # Only show next 5 periods
            forecast = f"""
    {period['name']}:
    Temperature: {period['temperature']}°{period['temperatureUnit']}
    Wind: {period['windSpeed']} {period['windDirection']}
    Forecast: {period['detailedForecast']}
    """
            forecasts.append(forecast)

        return "\n---\n".join(forecasts)


@workflow.defn
class GetWeatherChart:
    @workflow.run
    async def get_weather_chart(self, latitude: float, longitude: float, include_precipitation: bool = False) -> dict:
        """Get weather data and generate a chart visualization.

        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
            include_precipitation: If True, uses the advanced POST method with precipitation data

        Returns:
            A dict containing the forecast data and chart URL
        """
        # First get the forecast grid endpoint
        points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
        points_data = await workflow.execute_activity(
            make_nws_request,
            points_url,
            schedule_to_close_timeout=timedelta(seconds=40),
            retry_policy=retry_policy,
        )

        if not points_data:
            return {
                "success": False,
                "error": "Unable to fetch forecast data for this location.",
                "chart_url": None
            }

        # Get the forecast URL from the points response
        forecast_url = points_data["properties"]["forecast"]
        forecast_data = await workflow.execute_activity(
            make_nws_request,
            forecast_url,
            schedule_to_close_timeout=timedelta(seconds=40),
            retry_policy=retry_policy,
        )

        if not forecast_data:
            return {
                "success": False,
                "error": "Unable to fetch detailed forecast.",
                "chart_url": None
            }

        chart_url = await workflow.execute_activity(
            generate_weather_chart,
            args=[forecast_data, include_precipitation, 5],
            schedule_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy,
        )

        # Extract location info for the response
        location_props = points_data.get("properties", {})
        city = location_props.get("relativeLocation", {}).get("properties", {}).get("city", "Unknown")
        state = location_props.get("relativeLocation", {}).get("properties", {}).get("state", "Unknown")

        # Get first few periods for summary
        periods = forecast_data.get("properties", {}).get("periods", [])[:3]
        summary = []
        for period in periods:
            summary.append({
                "name": period["name"],
                "temperature": f"{period['temperature']}°{period['temperatureUnit']}",
                "shortForecast": period["shortForecast"]
            })

        return {
            "success": True,
            "location": f"{city}, {state}",
            "chart_url": chart_url,
            "summary": summary,
            "message": f"Weather chart generated for {city}, {state}"
        }