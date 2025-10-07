from temporalio.client import Client
from temporalio.worker import Worker

async def run_worker():
    # Connect to Temporal server (change address if using Temporal Cloud)
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="invoice-task-queue",
        workflows=[InvoiceWorkflow],
        activities=[payment_gateway],
    )
    print("Worker started. Listening for workflows...")
    await worker.run()