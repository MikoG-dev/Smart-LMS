from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    phone_number: str
    password: str
    role: str = "student"
    department_id: Optional[int] = None
    year_level: Optional[int] = None

class UserOut(BaseModel):
    id: int
    full_name: str
    phone_number: str
    role: str
    is_verified: bool
    points: int 

    class Config:
        from_attributes = True 

class Token(BaseModel):
    access_token: str
    token_type: str