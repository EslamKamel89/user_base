from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class UserBase(BaseModel):
    name:str
    email:str
    
    @field_validator('name')
    @classmethod
    def validate_name(cls , v:str) : 
        if not v or len(v.strip()) < 2 :
            raise ValueError('name must be at least 2 chars')
        return v.strip()
    
    @field_validator('email')
    @classmethod
    def validate_email(cls , v:str)->str : 
        v = v.strip().lower()
        if '@' not in v or '.' not in v :
            raise ValueError('invalid email format')
        return v

class UserCreate(UserBase):
    password:str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls , val:str) :
        if len(val) < 5 : 
            raise ValueError('password must be at least 5 chars')
        return val
        

class UserUpdate(BaseModel):
    name:Optional[str] = None
    email:Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls,v:str|None)->str|None:
        if v is None : 
            return None 
        if len(v.strip())< 2 :
            raise ValueError('name must be at least 2 chars')
        return v.strip()
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v:str|None)->str|None :
        if v is None :
            return None 
        if '@' not in v or '.'  not in v :
            raise ValueError('invalid email format')
        return v
    
class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name:str
    email :str
    created_at:datetime | None = None
    updated_at:datetime | None = None