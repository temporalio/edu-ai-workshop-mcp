import os
import random
import urllib.request
import json
from typing import Dict
from temporalio import activity
from temporalio.exceptions import ApplicationError

@activity.defn
async def payment_gateway(line: dict) -> bool:
    activity.logger.info("Paying %s", line.get("description"))
    # Simulate payment processing
    activity.logger.info("Payment succeeded")
    return True

@activity.defn
async def convert_currency(
    amount: float, from_currency: str = "EUR", to_currency: str = "USD"
) -> Dict:
    """Convert invoice amount between currencies using live exchange rates."""

    activity.logger.info(f"Converting {amount} from {from_currency} to {to_currency}")

    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())

        if to_currency.upper() not in data["rates"]:
            raise ApplicationError(
                f"Currency {to_currency} not supported", non_retryable=True
            )

        rate = data["rates"][to_currency.upper()]
        converted = amount * rate

        result = {
            "original_amount": amount,
            "from_currency": from_currency.upper(),
            "to_currency": to_currency.upper(),
            "exchange_rate": rate,
            "converted_amount": round(converted, 2),
            "timestamp": data["date"],
        }
        return result
    except Exception as e:
        activity.logger.error(f"Failed to fetch exchange rate: {str(e)}")