from pydantic import BaseModel


class ChatRequest(BaseModel):
    lead_id: int
    message: str


class ChatResponse(BaseModel):
    lead_id: int
    response: str