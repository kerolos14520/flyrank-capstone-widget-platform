import httpx
from typing import Dict, Any

async def send_webhook_notification(webhook_url: str, payload: Dict[str, Any]):
    """
    Executes an asynchronous HTTP POST to an external receiver.
    Runs entirely in the background without holding up client responses.
    """
    if not webhook_url:
        return

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.post(webhook_url, json=payload)
            print(f"[WEBHOOK LOG] Dispatched to {webhook_url} | Status Code: {response.status_code}")
        except Exception as err:
            print(f"[WEBHOOK ERROR] Delivery failed: {err}")