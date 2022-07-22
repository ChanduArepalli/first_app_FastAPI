from typing import Union

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    first_name: str = None
    last_name: str = None


class LoginSchema(BaseModel):
    username: str
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class Token(UserOut):
    access_token: str = None
    # token_type: str = None