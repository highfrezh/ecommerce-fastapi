from fastapi import APIRouter, Depends, HTTPException
from services.product_service import list_products, get_product
from database.models import User
from sqlalchemy.orm import Session
from database.session import get_db

router = APIRouter(prefix="/products", tags=["products"])


# Public endpoint
@router.get("/")
def browse_products(
    db: Session = Depends(get_db)
):
    return list_products(db)

# User-only endpoint
@router.get("/{product_id}")
def view_product_details(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product