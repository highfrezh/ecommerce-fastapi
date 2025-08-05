from fastapi import APIRouter, Depends, HTTPException
from services.order_service import get_user_orders
from schemas.order import OrderCreate, OrderOut
from core.security import get_current_ordinary_user
from database.models import User
from sqlalchemy.orm import Session
from database.session import get_db
from services.order_service import create_order_and_init_payment, verify_and_update_order_status

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/")
async def user_place_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_ordinary_user),
    ):

    return await create_order_and_init_payment(db, current_user, data)

@router.get("/verify")
async def verify_payment(reference: str, db: Session = Depends(get_db)):
    return await verify_and_update_order_status(reference, db)

@router.get("/", response_model=list[OrderOut])
def user_view_orders(
    current_user: User = Depends(get_current_ordinary_user),
    db: Session = Depends(get_db),
    ):
    return get_user_orders(db, current_user.id)