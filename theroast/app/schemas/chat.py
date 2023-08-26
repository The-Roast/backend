from typing import Optional, List
from pydantic import BaseModel, UUID4
from datetime import datetime

class ChatBase(BaseModel):
    type: Optional[str]
    content: Optional[str]

class ChatCreate(ChatBase):
    type: str
    content: str

class ChatUpdate(ChatBase):
    pass

class ChatInDBBase(ChatBase):
    type: str
    content: str
    created_at: datetime

class Chat(ChatInDBBase):
    newsletter_uuid: UUID4

class ChatInDB(ChatInDBBase):
    newsletter_uuid: UUID4

class Conversation(BaseModel):
    newsletter_uuid: UUID4
    log: List[ChatInDBBase]