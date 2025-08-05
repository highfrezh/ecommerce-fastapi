from pydantic import BaseModel, HttpUrl
from typing import Optional

class ProductBase(BaseModel):
    name: Optional[str] 
    price: Optional[float] 
    description: Optional[str]
    image_url: Optional[HttpUrl] = None 

class ProductCreate(ProductBase):
    stock: Optional[int]

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None  

class ProductOut(ProductBase):
    id: int
    stock: Optional[int]
    image_url: Optional[HttpUrl] = None  

    class Config:
        from_attributes = True