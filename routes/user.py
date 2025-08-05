from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from database.models import User
from schemas.user import UserOut, Profile, ProfileCreate, ProfileUpdate
from core.security import get_current_ordinary_user
from services.user_service import create_profile, get_user_profile, update_profile
from sqlalchemy.orm import Session
from database.session import get_db
from typing import Optional


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model= UserOut)
def read_current_user(current_user: User = Depends(get_current_ordinary_user)):
    return current_user

@router.post("/profile", response_model=Profile, status_code=201)
async def create_user_profile(
    firstname: str = Form(...),
    lastname: str = Form(...),
    address: str = Form(...),
    country: str = Form(...),
    phonenumber: str = Form(...),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_ordinary_user),
    db: Session = Depends(get_db)
    ):

    profile_data = ProfileCreate(
        firstname=firstname,
        lastname=lastname,
        address=address,
        country=country,
        phonenumber=phonenumber
    )
    return await create_profile(db, profile_data, current_user.id, image)

@router.put("/profile", response_model=Profile)
async def update_user_profile(
    firstname: Optional[str] = Form(None),
    lastname: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    phonenumber: Optional[str] = Form(None),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_ordinary_user),
    db: Session = Depends(get_db)
):
    profile_data = ProfileUpdate(
        firstname=firstname,
        lastname=lastname,
        address=address,
        country=country,
        phonenumber=phonenumber
    )
    return await update_profile(db, profile_data, current_user.id, image)

@router.get("/profile", response_model=Profile)
def get_my_profile(
    current_user: User = Depends(get_current_ordinary_user),
    db: Session = Depends(get_db)
):
    return get_user_profile(db, current_user.id)


#Basic user info can't be update

# @router.patch("/me")
# def update_current_user(
#     user_data: UserUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_ordinary_user),
# ):
#     return update_user(db, current_user.id, user_data)