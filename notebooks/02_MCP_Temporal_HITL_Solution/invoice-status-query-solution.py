from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
# sandboxed=False is a Notebook only requirement. You normally don't do this
@workflow.defn(sandboxed=False)
class InvoiceWorkflow:
    def __init__(self) -> None:
        self.approved: bool | None = None
        self.status: str = "INITIALIZING"

    @workflow.signal
    async def ApproveInvoice(self) -> None:
        self.approved = True

    @workflow.signal
    async def RejectInvoice(self) -> None:
        self.approved = False

    @workflow.query
    async def GetInvoiceStatus(self) -> str:
        return self.status

    @workflow.run
    async def run(self, invoice: dict) -> str:
        self.status = "PENDING-APPROVAL"

        workflow.logger.info(
            f"Waiting for approval for invoice {invoice.get('invoice_id')}"
        )
        # Wait for the approval signal

        await workflow.wait_condition(
            lambda: self.approved is not None,
            timeout=timedelta(days=5),
        )

        if not self.approved:
            workflow.logger.info("REJECTED")
            self.status = "REJECTED"
            return "REJECTED"

        self.status = "APPROVED"
        # Process each line item
        for line in invoice.get("lines", []):
            # Simple delay - wait 2 seconds before processing
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

        self.status = "PAID"
        return self.status
