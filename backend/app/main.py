from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .agent import agent, FALLBACK_MEMORY
from .demo_data import CUSTOMERS
from .models import ChatRequest, ChatResponse, Customer, MemoryItem

app = FastAPI(title="MemoryDesk AI", version="0.2.0")

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

@app.post("/api/demo/seed")
async def seed_demo():
    customer = next(c for c in CUSTOMERS if c.id == "c_rahul")
    seed = (
        f"Customer {customer.name} from {customer.company} uses {customer.device}. "
        "Previous support issue: the printer repeatedly disconnected from Wi-Fi. "
        "Troubleshooting already attempted: router restart and firmware update. "
        "Successful resolution: reinstalling the network driver. "
        "Customer prefers step-by-step instructions and does not want repeated troubleshooting."
    )
    await agent.hindsight.retain(seed, {
        "customer_id": customer.id,
        "source": "demo_seed",
    })
    FALLBACK_MEMORY[customer.id] = [{
        "id": "demo-seed-1",
        "type": "experience",
        "text": seed,
    }]
    return {"ok": True, "message": "Demo memory seeded for Rahul Sharma."}

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
