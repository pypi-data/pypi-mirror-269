from etiket_client.remote.endpoints.models.schema_base import SchemaData, SchemaAttributes
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

import datetime, uuid

class SchemaBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid : uuid.UUID
    name : str
    description: str = Field(default='')
    schema_ : SchemaData = Field(alias='schema')

class SchemaCreate(SchemaBase):
    pass

class SchemaRead(SchemaBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    created: datetime.datetime
    modified: datetime.datetime

class SchemaUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name : Optional[str] = Field(default=None)
    description : Optional[str] = Field(default=None)
    schema_ : Optional[SchemaData] = Field(alias='schema', default=None)

class SchemaDelete(BaseModel):
    uuid: uuid.UUID