import httpx
from typing import Dict, Any, Optional

GEO_PROVIDER_A = "https://ip-api.com/json/"
GEO_PROVIDER_B = "https://ipapi.co/"

async def resolve_ip_location(ip_address: str) -> Dict[str, Optional[str]]:
    """
    Attempts to resolve an IP address to country and city using a primary provider,
    falling back to a secondary provider if the first fails or times out.
    """
    # Bypass loopback / local addresses for testing
    if ip_address in ("127.0.0.1", "::1", "localhost"):
        return {"country": "Local Development", "city": "Localhost"}

    async with httpx.AsyncClient(timeout=3.0) as client:
        # Attempt Primary Provider (Provider A: ip-api)
        try:
            response = await client.get(f"{GEO_PROVIDER_A}{ip_address}")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {
                        "country": data.get("country"),
                        "city": data.get("city")
                    }
        except Exception:
            pass  # Fall through to Provider B on any network/timeout error

        # Attempt Secondary Provider (Provider B: ipapi.co)
        try:
            response = await client.get(f"{GEO_PROVIDER_B}{ip_address}/json/")
            if response.status_code == 200:
                data = response.json()
                if not data.get("error"):
                    return {
                        "country": data.get("country_name"),
                        "city": data.get("city")
                    }
        except Exception:
            pass  # Fall through to fail-safe default

    # Fail-safe fallback if both providers fail
    return {"country": "Unknown", "city": "Unknown"}