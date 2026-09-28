import httpx
from typing import Any
from .config import settings

class HindsightClient:
    def __init__(self) -> None:
        self.base = settings.hindsight_base_url.rstrip("/")
        self.bank_id = settings.hindsight_bank_id

    async def retain(self, text: str, metadata: dict[str, Any] | None = None) -> None:
        payload = {
            "bank_id": self.bank_id,
            "content": text,
            "metadata": metadata or {},
        }
        async with httpx.AsyncClient(timeout=15) as client:
            # Hindsight deployments can expose slightly different routes.
            # The default route below follows the current REST style; adjust
            # HINDSIGHT_BASE_URL if your cloud/self-hosted instance uses a prefix.
            for path in ("/v1/memory/retain", "/retain"):
                try:
                    r = await client.post(f"{self.base}{path}", json=payload)
                    if r.status_code < 400:
                        return
                except httpx.HTTPError:
                    pass
        # Fail softly in demo mode: the local fallback keeps the UI usable.

    async def recall(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        payload = {
            "bank_id": self.bank_id,
            "query": query,
            "limit": limit,
        }
        async with httpx.AsyncClient(timeout=15) as client:
            for path in ("/v1/memory/recall", "/recall"):
                try:
                    r = await client.post(f"{self.base}{path}", json=payload)
                    if r.status_code < 400:
                        data = r.json()
                        if isinstance(data, dict):
                            items = data.get("memories") or data.get("results") or []
                        else:
                            items = data
                        return items if isinstance(items, list) else []
                except (httpx.HTTPError, ValueError):
                    pass
        return []
