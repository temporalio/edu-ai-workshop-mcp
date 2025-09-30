import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import InvoiceWorkflow, ConvertCurrencyWorkflow
from activities import payment_gateway, convert_currency

async def main():
    client = await Client.connect(os.getenv("TEMPORAL_ADDRESS", "localhost:7233"))
    worker = Worker(
        client,
        task_queue="invoice-task-queue",
        workflows=[InvoiceWorkflow, ConvertCurrencyWorkflow],
        activities=[payment_gateway, convert_currency],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
