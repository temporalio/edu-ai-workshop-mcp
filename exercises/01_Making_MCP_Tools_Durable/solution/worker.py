import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import GetForecast, GetWeatherChart
from activities import make_nws_request, generate_weather_chart

async def main():
    # Connect to Temporal server (change address if using Temporal Cloud)
    client = await Client.connect("localhost:7233")

    # register both workflows and the activities
    worker = Worker(
        client,
        task_queue="weather-task-queue",
        workflows=[GetForecast, GetWeatherChart],
        activities=[make_nws_request, generate_weather_chart],
    )
    print("Worker started. Listening for workflows...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
