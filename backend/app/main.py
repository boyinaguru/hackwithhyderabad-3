from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .agent import agent
from .demo_data import CUSTOMERS
from .models import ChatRequest, ChatResponse, Customer, MemoryItem

app = FastAPI(title="MemoryDesk AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"ok": True, "service": "MemoryDesk AI"}

@app.get("/api/customers", response_model=list[Customer])
async def customers():
    return CUSTOMERS

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    customer = next((c for c in CUSTOMERS if c.id == req.customer_id), None)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    answer, memories = await agent.chat(req.customer_id, customer.model_dump(), req.message)

    normalized = []
    for i, m in enumerate(memories[:6]):
        normalized.append(
            MemoryItem(
                id=str(m.get("id", i)),
                type=str(m.get("type", "memory")),
                text=str(m.get("text") or m.get("content") or m),
                score=m.get("score"),
            )
        )

    return ChatResponse(
        answer=answer,
        memories=normalized,
        used_memory=bool(memories),
        mode="hindsight" if memories else "new-context",
    )
