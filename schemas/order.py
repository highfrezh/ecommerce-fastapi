from pydantic import BaseModel
from typing import Optional
from enum import Enum
from schemas.product import ProductOut

# Order Status Options
class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Base Order Schema
class OrderBase(BaseModel):
    product_id: int
    quantity: int

# Request: Place Order
class OrderCreate(OrderBase):
    pass

# Request: Update Order Status (Admin-only)
class OrderUpdateStatus(BaseModel):
    status: OrderStatus

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    description: str
    image_url: str
    
    class Config:
        from_attributes = True
        exclude = {"stock"} 

class OrderOut(BaseModel):
    id: int
    quantity: int
    status: str
    product: ProductOut  # Nested product schema
    