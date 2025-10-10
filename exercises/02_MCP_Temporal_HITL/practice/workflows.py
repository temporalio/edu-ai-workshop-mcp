from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from activities import payment_gateway, convert_currency

@workflow.defn
class ConvertCurrencyWorkflow:
    def __init__(self) -> None:
        self.db_entry_confirmed: bool = False
        self.converted_amount: float | None = None

    # TODO Part C: Create a Signal that sets the value of `db_entry_confirmed` 
    # (already set for you) to `True`.

    # TODO Part B: Create a Query that gets the conversion amount 
    # and returns the current value of `converted_amount` (already set for you).

    @workflow.run
    async def run(self, amount: float, from_currency: str, to_currency: str) -> float:
        # Normalize currency codes to uppercase
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        # Validate currency codes (basic check for 3-letter codes)
        if len(from_currency) != 3 or len(to_currency) != 3:
            raise ApplicationError("Currency codes must be 3 letters")

        # Execute the conversion activity
        conversion_result = await workflow.execute_activity(
            # TODO Part A: Call your `convert_currency` Activity
            args=[], # TODO Part A: Pass in the arguments of `amount`, `from_currency`, `to_currency`
            # TODO Part A: Set your Start-to-Close Timeout to be 30 seconds.
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=10),
                maximum_attempts=3,
            ),
        )
        self.converted_amount = conversion_result["converted_amount"]
        workflow.logger.info(
            f"Converted {amount} {from_currency} to {self.converted_amount:.2f} {to_currency}"
        )
        
        # Wait for confirmation that the amount has been added to the database
        workflow.logger.info("Waiting for confirmation that amount is added to Dummy database...")
        # TODO Part C: Use `workflow.wait_condition` to pause execution until one of 2 conditions
        # `self.db_entry_confirmed` becomes `True`, or
        # 5 days pass (whichever happens first).

        workflow.logger.info("Dummy Database add confirmed. Completing workflow.")
        # TODO Part B: Return the value of the `converted_amount`.

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
