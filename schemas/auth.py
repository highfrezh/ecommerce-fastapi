
from pydantic import BaseModel, EmailStr

# Request: User Registration
class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False  # Default False (only admins can promote others)

class UserRegisterOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True 
        exclude = {"hashed_password", "is_admin"}  

# Request: User Login
class UserLoginRequest(BaseModel):
    username: str
    password: str

# Response: Token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"