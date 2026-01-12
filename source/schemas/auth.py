from pydantic import BaseModel
from typing import Optional

class RegisterRequest(BaseModel):
    username: str
    role: Optional[str] = "admin"
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    id: str
    role: str
    username: str
    
    model_config = {
        "from_attributes": True
    }

class AuthResponse(BaseModel):
    user : UserInfo
    token: str
    token_type: str = "bearer"