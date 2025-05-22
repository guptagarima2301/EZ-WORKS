from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "client"  # Optional role, default client

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FileUpload(BaseModel):
    filename: str
    content_type: str
