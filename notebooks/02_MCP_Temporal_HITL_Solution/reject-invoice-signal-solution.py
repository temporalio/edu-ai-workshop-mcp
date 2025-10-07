## Let's add Signals to approve or reject invoices!
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# sandboxed=False is a Notebook only requirement. You normally don't do this
@workflow.defn(sandboxed=False)
class InvoiceWorkflow:
    def __init__(self) -> None:
        self.approved: bool | None = None

    @workflow.signal
    async def ApproveInvoice(self) -> None:
        self.approved = True

    @workflow.signal
    async def RejectInvoice(self) -> None:
        self.approved = False

    @workflow.run
    async def run(self, invoice: dict) -> str:
        # Wait for the approval signal
        await workflow.wait_condition(
            lambda: self.approved is not None,
            timeout=timedelta(days=5),
        )

        # Process each line item
        for line in invoice.get("lines", []):
            await workflow.sleep(timedelta(seconds=2))

            # Try to process payment
            try:
                await workflow.execute_activity(
                    payment_gateway,
                    line,
                    start_to_close_timeout=timedelta(seconds=30),
                    retry_policy=RetryPolicy(
                        initial_interval=timedelta(seconds=1),
                        maximum_interval=timedelta(seconds=30),
                        maximum_attempts=3,
                    ),
                )
            except Exception:
                workflow.logger.error(f"Failed to process line item: {line}")

        return "COMPLETED"