from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    
    orders = relationship("Order", back_populates="user", cascade="all, delete")
    profile = relationship("Profile", back_populates="user", uselist=False) 

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    address = Column(String(200))
    country = Column(String(50))
    phonenumber = Column(String(20))
    profile_image = Column(String(255))  # Store image path or URL
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="profile")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    stock = Column(Integer)
    image_url = Column(String, nullable=True)  

    orders = relationship("Order", back_populates="product", cascade="all, delete")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer)
    status = Column(String, default="pending")  # pending, completed, cancelled
    reference = Column(String, unique=True, nullable=True)
    amount = Column(Integer, nullable=False)
    
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    