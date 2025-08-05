from sqlalchemy.orm import Session
from database.models import User, Profile
from schemas.user import ProfileCreate, ProfileUpdate
from fastapi import HTTPException, status, UploadFile
import os
from tempfile import NamedTemporaryFile
from core.cloudinary import upload_profile_image
import cloudinary.uploader

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

async def upload_image(user_id: int, image: UploadFile):
        """Handles Cloudinary upload with cleanup"""
        try:
            with NamedTemporaryFile(delete=False, suffix=os.path.splitext(image.filename)[1]) as tmp:
                await image.seek(0)
                tmp.write(await image.read())
                tmp_path = tmp.name
            return upload_profile_image(tmp_path, str(user_id))
        finally:
            await image.close()
            if tmp_path:
                os.unlink(tmp_path)

def delete_image_if_exists(profile: Profile):
    """Delete old image if profile exists"""
    if profile and profile.profile_image:
        public_id = f"profile_images/user_{profile.user_id}"
        cloudinary.uploader.destroy(public_id)

async def create_profile(
    db: Session,
    profile_data: ProfileCreate,
    user_id: int,
    image: UploadFile = None
):
    # Check if profile already exists
    if db.query(Profile).filter(Profile.user_id == user_id).first():
        raise HTTPException(status_code=400, detail="Profile already exists")

    # Handle image upload
    image_url = await upload_image(user_id, image) if image else None

    # Create profile - explicitly map fields to avoid duplicates
    db_profile = Profile(
        firstname=profile_data.firstname,
        lastname=profile_data.lastname,
        address=profile_data.address,
        country=profile_data.country,
        phonenumber=profile_data.phonenumber,
        profile_image=image_url,  # Only set once here
        user_id=user_id
    )
    
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

async def update_profile(
    db: Session,
    profile_data: ProfileUpdate,
    user_id: int,
    image: UploadFile | None = None
):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Handle image update
    if image:
        delete_image_if_exists(profile)
        profile.profile_image = await upload_image(user_id, image)

    # Update only non-None fields
    for field, value in profile_data.model_dump(exclude_unset=True).items():
        if value is not None:  # Only update if the value is not None
            setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile

def get_user_profile(db: Session, user_id: int):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile


def list_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(User).offset(skip).limit(limit).all()
    return users