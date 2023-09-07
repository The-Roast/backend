from typing import Optional, List, Union
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
    created_at: Union[datetime, str]

class Chat(ChatInDBBase):
    newsletter_uuid: Optional[UUID4]
    created_at: datetime

class ChatInDB(ChatInDBBase):
    newsletter_uuid: Optional[UUID4]
    created_at: str

class Conversation(BaseModel):
    newsletter_uuid: UUID4
    log: List[ChatInDBBase]