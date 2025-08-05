import httpx
from core.config import settings

headers = {
    "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    "Content-Type": "application/json",
}


async def initialize_transaction(email: str, amount: int, callback_url: str):
    """
    Initiate a Paystack transaction.
    
    :param email: Customer email
    :param amount: Amount in kobo (₦1000 = 100000)
    :param callback_url: Where Paystack should redirect after payment
    :return: JSON response from Paystack
    """
    url = f"{settings.PAYSTACK_BASE_URL}/transaction/initialize"
    payload = {
        "email": email,
        "amount": amount,
        "callback_url": callback_url,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        return response.json()


async def verify_transaction(reference: str):
    """
    Verify a Paystack transaction by its reference.

    :param reference: The reference string returned by Paystack
    :return: JSON response from Paystack
    """
    url = f"{settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()
