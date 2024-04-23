from etiket_client.remote.endpoints.models.types import filestr, FileType, FileStatusLocal

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

import datetime, uuid

class FileBase(BaseModel):
    name : filestr
    filename : str
    uuid : uuid.UUID
    creator : str
    collected : datetime.datetime
    size : int
    type : FileType
    file_generator : Optional[str]
    version_id : int

    etag: Optional[str] = None
    status : FileStatusLocal
    
    local_path : str
    ntimes_accessed : int = 0
    synchronized : bool = Field(default=False)

class FileCreate(FileBase):
    ds_uuid : uuid.UUID

class FileRead(FileBase):
    model_config = ConfigDict(from_attributes=True)
    
    created: datetime.datetime
    modified: datetime.datetime
    
    last_accessed : Optional[datetime.datetime]
    ntimes_accessed : int
    synchronized : bool
    
class FileUpdate(BaseModel):
    file_generator : Optional[str] = None
    size : Optional[int] = None
    type : Optional[FileType] = None
    etag: Optional[str] = None
    status : Optional[FileStatusLocal] = None
    
    local_path : Optional[str] = None
    s3_link : Optional[str] = None
    s3_validity : Optional[datetime.datetime] = None
    last_accessed : Optional[datetime.datetime] = None
    ntimes_accessed : Optional[int] = None
    synchronized : bool = False

class FileSelect(BaseModel):
    uuid : uuid.UUID
    version_id : Optional[int] = Field(default=None) 

class FileSignedUploadLinks(BaseModel):
    upload_id : str
    part_size : int
    presigned_urls : List[str]