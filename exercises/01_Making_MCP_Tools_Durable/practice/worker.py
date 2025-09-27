import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import GetForecast, GetWeatherChart
# TODO Part C: Import your Activities.

async def main():
    # Connect to Temporal server (change address if using Temporal Cloud)
    client = await Client.connect("localhost:7233")

    # register both workflows and the activities
    worker = Worker(
        client,
        task_queue="weather-task-queue",
        workflows=[], # TODO Part C: Register your Workflows
        activities=[], # TODO Part C: Register your Activities
    )
    print("Worker started. Listening for workflows...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
