from etiket_client.remote.endpoints.models.types import usernamestr, UserType

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

import datetime

class UserBase(BaseModel):
    username: usernamestr
    firstname: str
    lastname: str
    email: EmailStr
    user_type: UserType = Field(default=UserType.standard_user)

    disable_on: Optional[datetime.datetime] = Field(default=None)

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    created: datetime.datetime
    modified: datetime.datetime
    