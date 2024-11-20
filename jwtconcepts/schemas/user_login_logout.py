# app/schemas.py
from pydantic import BaseModel
from typing import Optional
# Request schema for login
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    username: str
    email: str

# Response schema for JWT token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Schema for User (to return user data)
class UserResponse(BaseModel):
    username: str

    class Config:
        orm_mode = True  # Allow Pydantic to work with SQLAlchemy models
        
class Itemsc(BaseModel):
    name: str
    description: str
    price: float

class ItemBase(BaseModel):
    name: str
    description: str
    price: float

# Pydantic models for input/output validation
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(ItemCreate):
    id: int

    class Config:
        orm_mode = True



#Serializer Fields and Core Arguments:In FastAPI, you define models using Pydantic fields. You can specify types, validation, and default values directly in the model.
from pydantic import Field
class Serializer_fields(BaseModel):
    name: str
    description: str = Field(..., min_length=3)
    price: float