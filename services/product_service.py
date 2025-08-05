from sqlalchemy.orm import Session
from database.models import Product
from fastapi import UploadFile, HTTPException
from schemas.product import ProductCreate, ProductUpdate

from core.cloudinary import upload_product_image, delete_product_image

async def create_product(db: Session, product_data: ProductCreate, image: UploadFile = None):
    db_product = Product(**product_data.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    if image:
        db_product.image_url = await upload_product_image(image.file, db_product.id)
        db.commit()
        db.refresh(db_product)
    
    return db_product

async def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate,
    image: UploadFile = None
    ):
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if any fields are being updated
    update_data = product_data.model_dump(exclude_unset=True)
    if not update_data and image is None:
        raise HTTPException(status_code=400, detail="No fields to update")

    try:
        # Handle image update
        if image:
            if db_product.image_url:
                delete_product_image(product_id)
            db_product.image_url = await upload_product_image(image.file, product_id)

        # Update only provided fields
        for field, value in update_data.items():
            if value is not None:  # Still check for None in case
                setattr(db_product, field, value)

        db.commit()
        db.refresh(db_product)
        return db_product
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete image if exists
    if db_product.image_url:
        delete_product_image(product_id)
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}


def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return "Invalid product ID"
    return product


def list_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()