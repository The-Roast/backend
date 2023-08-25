from typing import Optional
from pydantic import BaseModel, UUID4

class ChatBase(BaseModel):
    newsletter_uuid: UUID4
    type: Optional[str]
    content: Optional[str]

class ChatCreate(ChatBase):
    type: str
    content: str

class ChatInDBBase(ChatBase):
    type: str
    content: str
