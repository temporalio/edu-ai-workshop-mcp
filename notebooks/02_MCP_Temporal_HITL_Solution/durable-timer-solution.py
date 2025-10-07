from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio import workflow

# sandboxed=False is a Notebook only requirement. You normally don't do this
@workflow.defn(sandboxed=False)
class InvoiceWorkflow:
    @workflow.run
    async def run(self, invoice: dict) -> str:
        # Process each line item
        for line in invoice.get("lines", []):
            await workflow.sleep(timedelta(seconds=2))
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
            except Exception as e:
                workflow.logger.error(f"Failed to process line item {line.get('item_id')}: {e}")
        return "COMPLETED"
