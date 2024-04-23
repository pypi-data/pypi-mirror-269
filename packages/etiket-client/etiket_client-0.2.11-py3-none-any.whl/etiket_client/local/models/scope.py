from etiket_client.local.models.schema import SchemaRead
from etiket_client.local.models.user_base import UserRead
from etiket_client.remote.endpoints.models.types import scopestr

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

import datetime, uuid


class ScopeBase(BaseModel):
    name : scopestr
    uuid : uuid.UUID
    description: str
    archived: bool

class ScopeCreate(ScopeBase):
    pass

class ScopeUpdate(BaseModel):
    name : Optional[scopestr] = None
    description: Optional[str] = None

class ScopeRead(ScopeBase):
    model_config = ConfigDict(from_attributes=True)
    
    created: datetime.datetime
    modified: datetime.datetime
    archived: bool
    
    schema_: Optional["SchemaRead"] = Field(alias="schema")

class ScopeReadWithUsers(ScopeRead):
    users : List["UserRead"]