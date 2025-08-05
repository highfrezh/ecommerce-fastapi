from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services.auth_service import (
    register_user,
    authenticate_user,
    generate_user_token
)
from schemas.auth import UserRegisterRequest, TokenResponse, UserLoginRequest,UserRegisterOut
from database.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

# Register a new user
@router.post("/register", response_model=UserRegisterOut)
def register(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    user = register_user(db, user_data)
    return user
    # token = generate_user_token(user)
    # return {"access_token": token, "token_type": "bearer"}

# Login (supports OAuth2 password flow)
@router.post("/login", response_model=TokenResponse)
def login(
    data: UserLoginRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, data.username, data.password)
    token = generate_user_token(user)
    return {"access_token": token, "token_type": "bearer"}