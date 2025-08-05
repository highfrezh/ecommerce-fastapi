from fastapi import APIRouter, Depends, status
from database.session import get_db
from database.models import User
from sqlalchemy.orm import Session
from schemas.password import PasswordChangeRequest
from services.password_service import change_user_password
from core.security import get_current_user

router = APIRouter(prefix="/pwd", tags=["password"])

@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return change_user_password(
        db=db,
        user=current_user,
        current_password=password_data.current_password,
        new_password=password_data.new_password
    )