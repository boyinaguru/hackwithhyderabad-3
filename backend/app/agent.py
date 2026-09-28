import httpx
from typing import Any
from .config import settings
from .hindsight import HindsightClient

FALLBACK_MEMORY: dict[str, list[dict[str, Any]]] = {}

SYSTEM_PROMPT = """You are MemoryDesk, a customer support agent.
You solve the current issue concisely and professionally.
Use remembered customer context when it is relevant.
Never claim a memory exists unless it appears in the supplied memory context.
When a previous successful fix is available, prefer it over repeating generic advice.
If important information is missing, ask one focused question.
"""

class SupportAgent:
    def __init__(self) -> None:
        self.hindsight = HindsightClient()

    async def chat(self, customer_id: str, customer: dict[str, Any], message: str) -> tuple[str, list[dict[str, Any]]]:
        query = f"Customer {customer['name']} at {customer['company']}. Current issue: {message}"
        memories = await self.hindsight.recall(query)

        if not memories:
            memories = FALLBACK_MEMORY.get(customer_id, [])

        memory_text = "\n".join(
            f"- {m.get('text') or m.get('content') or str(m)}"
            for m in memories[:6]
        )

        if settings.llm_api_key:
            answer = await self._llm_answer(customer, message, memory_text)
        else:
            answer = self._deterministic_answer(customer, message, memories)

        record = (
            f"Customer: {customer['name']} | Company: {customer['company']} | "
            f"Device: {customer['device']} | Interaction: {message} | "
            f"Agent response: {answer}"
        )

        await self.hindsight.retain(
            record,
            {"customer_id": customer_id, "company": customer["company"], "source": "support_interaction"},
        )

        FALLBACK_MEMORY.setdefault(customer_id, []).append({
            "id": f"fallback-{len(FALLBACK_MEMORY.get(customer_id, []))+1}",
            "type": "interaction",
            "text": record,
        })

        return answer, memories

    async def _llm_answer(self, customer: dict[str, Any], message: str, memory_text: str) -> str:
        url = f"{settings.llm_base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": settings.llm_model,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content":
                    f"Customer: {customer['name']} ({customer['company']})\n"
                    f"Device: {customer['device']}\n"
                    f"Remembered context:\n{memory_text or 'No useful memory found.'}\n\n"
                    f"Current message: {message}"
                }
            ],
        }
        async with httpx.AsyncClient(timeout=45) as client:
            r = await client.post(
                url,
                json=payload,
                headers={"Authorization": f"Bearer {settings.llm_api_key}"},
            )
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()

    def _deterministic_answer(self, customer: dict[str, Any], message: str, memories: list[dict[str, Any]]) -> str:
        text = message.lower()
        remembered = " ".join(
            str(m.get("text") or m.get("content") or "")
            for m in memories
        ).lower()

        if memories and ("printer" in text or "wifi" in text or "disconnect" in text):
            if "driver reinstall" in remembered:
                return (
                    f"I remember this customer previously had a connectivity issue on "
                    f"{customer['device']}. A driver reinstall was recorded as the successful "
                    f"fix, so I'd start there rather than repeat the router-reset steps."
                )
            return (
                f"I found relevant history for {customer['name']}. "
                f"Let's compare the current symptoms with the previous support interaction."
            )

        if memories:
            return (
                f"I found {len(memories)} relevant memory item(s) from this customer's history. "
                "I can use that context to avoid repeating steps and personalize the next action."
            )

        return (
            "I don't have useful prior context for this issue yet. "
            "Let's capture the device, symptoms, and what has already been tried."
        )

agent = SupportAgent()
