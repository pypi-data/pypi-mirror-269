from etiket_client.remote.endpoints.models.types import UserType

from etiket_client.local.models.user_base import UserBase, UserRead
from etiket_client.local.models.scope import ScopeRead

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserCreate(UserBase):
    pass
        
class UserReadWithScopes(UserRead):    
    scopes : List[ScopeRead]

class UserUpdate(BaseModel):
    firstname: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    user_type: Optional[UserType] = Field(default=None)  
