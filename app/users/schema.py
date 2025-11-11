from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.utils.validate import Validate


class UserBase(BaseModel):
    name:str
    email:str
    
    @field_validator('name')
    @classmethod
    def validate_name(cls , v:str|None)->str|None : 
        return Validate.strip_and_validate_name(v)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls , v:str|None)->str|None : 
        return Validate.strip_lower_validate_email(v)
        

class UserCreate(UserBase):
    password:str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls , v:str) :
        return Validate.validate_password(v)
        

class UserUpdate(BaseModel):
    name:Optional[str] = None
    email:Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls , v:str|None)->str|None : 
        return Validate.strip_and_validate_name(v)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls , v:str|None)->str|None : 
        return Validate.strip_lower_validate_email(v)
      
    
class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name:str
    email :str
    created_at:datetime | None = None
    updated_at:datetime | None = None


UserCreate.model_config = ConfigDict(
    json_schema_extra={
        "example" : {
            "name": "Eslam Kamel",
            "email": "eslam@example.com",
            "password": "secret123"
        }
    }
)

UserUpdate.model_config = ConfigDict(
    json_schema_extra={
        'example' : {"name": "Eslam K.", "email": "eslam.k@example.com"}
    }
)

UserRead.model_config = ConfigDict(
    json_schema_extra={
        "example" : {
            "id": 1,
            "name": "Eslam Kamel",
            "email": "eslam@example.com",
            "created_at": "2025-11-09T10:00:00+00:00",
            "updated_at": "2025-11-09T10:05:00+00:00"
        }
    }
)