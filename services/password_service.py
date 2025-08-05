from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database.models import User
from core.security import verify_password, get_password_hash

def change_user_password(
    db: Session,
    user: User,
    current_password: str,
    new_password: str
):
    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Prevent password reuse (optional but recommended)
    if verify_password(new_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )
    
    # Update password
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    return {"message": "Password updated successfully"}