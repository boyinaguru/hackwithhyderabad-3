from pydantic import BaseModel, Field
from typing import Any, Optional

class Customer(BaseModel):
    id: str
    name: str
    company: str
    email: str
    device: str
    open_ticket: Optional[str] = None

class ChatRequest(BaseModel):
    customer_id: str
    message: str = Field(min_length=1, max_length=4000)

class MemoryItem(BaseModel):
    id: str
    type: str
    text: str
    score: Optional[float] = None

class ChatResponse(BaseModel):
    answer: str
    memories: list[MemoryItem]
    used_memory: bool
    mode: str
