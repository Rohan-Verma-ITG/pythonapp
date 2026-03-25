from datetime import datetime
from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: int
    role: str
    body: str
    channel: str = 'shopify_chat'


class ConversationCreate(BaseModel):
    customer_id: int | None = None
    channel: str = 'shopify_chat'
    subject: str | None = None


class TicketCreate(BaseModel):
    conversation_id: int
    assignee_id: int | None = None
    priority: str = 'normal'


class TicketUpdate(BaseModel):
    status: str | None = None
    assignee_id: int | None = None
    priority: str | None = None


class AIReplyRequest(BaseModel):
    conversation_id: int
    message: str


class BaseResponse(BaseModel):
    id: int
    created_at: datetime | None = None
