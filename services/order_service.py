from sqlalchemy.orm import Session
from database.models import Order, Product
from schemas.order import OrderCreate
from sqlalchemy.orm import joinedload
from database.models import User
import uuid
from fastapi import HTTPException
from services.paystack_service import initialize_transaction, verify_transaction

# def place_order(db: Session, user_id: int, product_id: int, quantity: int):
#     # Check product stock
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if not product or product.stock < quantity:
#         return None
    
#     # Reduce stock
#     product.stock -= quantity
#     db.add(product)
    
#     # Create order
#     order = Order(
#         user_id=user_id,
#         product_id=product_id,
#         quantity=quantity,
#         status="pending"
#     )
#     db.add(order)
#     db.commit()
#     db.refresh(order)
#     return order

async def create_order_and_init_payment(
    db: Session, user: User, data: OrderCreate
):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product or product.stock < data.quantity:
        raise HTTPException(status_code=400, detail="Invalid product or insufficient stock")

    amount_kobo = product.price * data.quantity * 100
    callback_url = "http://localhost:8000/orders/verify"

    # Call Paystack
    payment = await initialize_transaction(user.email, amount_kobo, callback_url)

    if not payment["status"]:
        raise HTTPException(status_code=400, detail=payment["message"])

    # Get Paystack reference after response
    reference = payment["data"]["reference"]

    # Reduce stock and create order
    product.stock -= data.quantity
    db.add(product)

    order = Order(
        user_id=user.id,
        product_id=data.product_id,
        quantity=data.quantity,
        amount=amount_kobo,
        status="pending",
        reference=reference
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    return {
        "message": "Order created. Redirect user to Paystack to complete payment.",
        "order_id": order.id,
        "amount": amount_kobo / 100,
        "checkout_url": payment["data"]["authorization_url"]
    }


async def verify_and_update_order_status(reference: str, db: Session):
    result = await verify_transaction(reference)

    if not result["status"]:
        raise HTTPException(status_code=400, detail="Verification failed")

    data = result["data"]
    if data["status"] == "success":
        order = db.query(Order).filter(Order.reference == reference).first()
        if order:
            order.status = "paid"
            db.commit()
            return {
                "message": "Payment verified",
                "order_id": order.id,
                "amount_paid": data["amount"] / 100,
                "customer_email": data["customer"]["email"]
            }

        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Payment not completed", "status": data["status"]}

def get_user_orders(db: Session, user_id: int):
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .options(joinedload(Order.product))
        .all()
    )

def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order

def list_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()