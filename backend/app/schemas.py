from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class AccountCreate(BaseModel):
    platform: str
    username: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class AccountUpdate(BaseModel):
    platform: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class AccountResponse(BaseModel):
    id: int
    platform: str
    username: str
    password: str
    email: Optional[str]
    phone: Optional[str]
    notes: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
