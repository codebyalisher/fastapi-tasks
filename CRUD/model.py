# models.py
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

# Pydantic model for User
class User(BaseModel):
    name: str
    email: str
    password: str
    address: Optional[str] = None

    class Config:
        # Pydantic will handle ObjectId serialization to string
        json_encoders = {
            ObjectId: str
        }
