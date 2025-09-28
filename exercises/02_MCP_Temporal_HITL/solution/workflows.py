from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from activities import payment_gateway, convert_currency

@workflow.defn
class PayLineItem:
    @workflow.run
    async def run(self, line: dict) -> str:
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
                    non_retryable_error_types=["INSUFFICIENT_FUNDS"],
                ),
            )
            return "SUCCESS"
        except Exception:
            return "FAILED"
            
@workflow.defn
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
    def GetInvoiceStatus(self) -> str:
        return self.status

    @workflow.run
    async def run(self, invoice: dict) -> str:
        self.status = "PENDING-APPROVAL"
        workflow.logger.info(
            f"Waiting for approval for invoice {invoice.get('invoice_id')}"
        )

        # Check if currency conversion is needed
        if invoice.get("convert_currency"):
            conversion_params = invoice.get("convert_currency")
            amount_to_convert = conversion_params.get("amount", 0)

            conversion_result = await workflow.execute_activity(
                convert_currency,
                args=[
                    amount_to_convert,
                    conversion_params.get("from_currency"),
                    conversion_params.get("to_currency"),
                ],
                start_to_close_timeout=timedelta(seconds=30),
            )
            workflow.logger.info(f"Currency conversion result: {conversion_result}")
            invoice["currency_conversion"] = conversion_result
            invoice["original_amount"] = invoice.get("total_amount")
            invoice["total_amount"] = conversion_result["converted_amount"]

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
        workflow.logger.info(
            f"Invoice {invoice.get('invoice_id')} approved, processing line items"
        )
        # Process each line item in parallel
        results = []
        for line in invoice.get("lines", []):
            handle = await workflow.start_child_workflow(
                PayLineItem.run,
                line,
            )
            results.append(handle)

        self.status = "PAID"
        # Wait for all line items to complete
        for handle in results:
            await handle

        return self.status