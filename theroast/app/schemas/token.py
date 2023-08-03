from typing import Optional
from pydantic import BaseModel, UUID4
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    exp: Optional[int] = None
    sub: Optional[UUID4] = None