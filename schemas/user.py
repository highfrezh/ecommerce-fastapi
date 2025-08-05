from pydantic import BaseModel, EmailStr
from typing import Optional

# Base User Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Request: User Registration
class UserCreate(UserBase):
    password: str

# Request: User Profile Update
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True 
        exclude = {"hashed_password", "is_admin"}  

class ProfileBase(BaseModel):
    firstname: str
    lastname: str
    address: str
    country: str
    phonenumber: str
    profile_image: Optional[str] = None

# class ProfileCreate(ProfileBase):
#     pass

class Profile(ProfileBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True  

class ProfileBase(BaseModel):
    firstname: str
    lastname: str
    address: str
    country: str
    phonenumber: str
    profile_image: Optional[str] = None

class ProfileCreate(ProfileBase):
    firstname: str
    lastname: str
    address: str
    country: str
    phonenumber: str

class ProfileUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    phonenumber: Optional[str] = None