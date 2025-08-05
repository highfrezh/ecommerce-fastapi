from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from services.product_service import (
    create_product, get_product, update_product, delete_product, list_products
)
from services.user_service import list_users
from services.order_service import update_order_status, list_orders
from schemas.product import ProductCreate, ProductUpdate, ProductOut
from schemas.order import OrderUpdateStatus
from schemas.user import UserOut
from core.security import get_current_admin
from database.models import User
from sqlalchemy.orm import Session
from database.session import get_db
from typing import Optional


router = APIRouter(prefix="/admin", tags=["admin"])


# Product CRUD
@router.get("/products/")
def admin_list_products(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    return list_products(db, skip=skip, limit=limit)

@router.get("/products/{product_id}")
def admin_get_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return get_product(db, product_id)

@router.post("/products/", response_model=ProductOut)
async def admin_create_product(
    name: str = Form(...),
    price: float = Form(...),
    description: str = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    
    # print(f"Image received - filename: {image.filename}, size: {image.size}")

    product_data = ProductCreate(
        name=name,
        price=price,
        description=description,
        stock=stock
    )
    return await create_product(db, product_data, image)

@router.put("/products/{product_id}", response_model=ProductOut)
async def admin_update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    description: Optional[str] = Form(None),
    stock: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    product_data = ProductUpdate(
        name=name,
        price=price,
        description=description,
        stock=stock
    )
    return await update_product(db, product_id, product_data, image)


@router.delete("/products/{product_id}")
def admin_delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return delete_product(db, product_id)


# User Management
@router.get("/users/", response_model=list[UserOut])
def admin_list_users(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
    ):
    return list_users(db, skip, limit)

# Order Management
@router.get("/orders/")
def admin_list_orders(
    admin: User = Depends(get_current_admin),
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),

    ):
    return list_orders(db, skip, limit)

@router.patch("/orders/{order_id}")
def admin_update_order_status(
    order_id: int,
    order_status: OrderUpdateStatus,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return update_order_status(db, order_id, order_status.status)