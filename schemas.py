from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: EmailStr
    phone: str
    password: str
    name: str
    city: str

class UserOut(BaseModel):
    id: int
    username: str
    phone: str
    name: str
    city: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    phone: Optional[str]
    name: Optional[str]
    city: Optional[str]

class Token(BaseModel):
    access_token: str

class AdCreate(BaseModel):
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str

class AdOut(AdCreate):
    id: int
    user_id: int
    total_comments: Optional[int] = 0

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_id: int

    class Config:
        orm_mode = True
