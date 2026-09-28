import asyncio
from typing import Any

from hindsight_client import Hindsight
from .config import settings


class HindsightClient:
    """Async-friendly wrapper around the official Hindsight Python SDK."""

    def __init__(self) -> None:
        kwargs = {"base_url": settings.hindsight_base_url, "timeout": 30.0}
        if settings.hindsight_api_key:
            kwargs["api_key"] = settings.hindsight_api_key
        self.client = Hindsight(**kwargs)
        self.bank_id = settings.hindsight_bank_id
        self._bank_ready = False

    async def _ensure_bank(self) -> None:
        if self._bank_ready:
            return
        try:
            await asyncio.to_thread(
                self.client.create_bank,
                bank_id=self.bank_id,
                name="MemoryDesk Customer Support",
            )
        except Exception:
            # Existing banks are expected to raise on create; harmless.
            pass
        self._bank_ready = True

    async def retain(self, text: str, metadata: dict[str, Any] | None = None) -> None:
        await self._ensure_bank()
        try:
            await asyncio.to_thread(
                self.client.retain,
                bank_id=self.bank_id,
                content=text,
                context=(metadata or {}).get("source", "support_interaction"),
            )
        except Exception:
            # Local fallback keeps the demo usable during service outages.
            pass

    async def recall(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        await self._ensure_bank()
        try:
            result = await asyncio.to_thread(
                self.client.recall,
                bank_id=self.bank_id,
                query=query,
                max_tokens=max(512, limit * 500),
                budget="mid",
            )
            return [
                {
                    "id": getattr(item, "id", ""),
                    "type": getattr(item, "type", "memory"),
                    "text": getattr(item, "text", ""),
                    "score": getattr(item, "score", None),
                }
                for item in getattr(result, "results", [])[:limit]
            ]
        except Exception:
            return []
