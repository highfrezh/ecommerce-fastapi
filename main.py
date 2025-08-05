from fastapi import FastAPI
from routes import auth, user, admin, order, product, password
from fastapi.middleware.cors import CORSMiddleware
from database.session import engine, Base
from core.config import settings
from services.auth_service import register_user
from schemas.auth import UserRegisterRequest
from database.session import get_db
from database.models import User
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(password.router)


def create_first_admin(db: Session):
    if settings.FIRST_ADMIN_EMAIL and not db.query(User).filter(User.is_admin).first():
        admin_user = UserRegisterRequest(
            username=settings.FIRST_ADMIN_USERNAME,
            email=settings.FIRST_ADMIN_EMAIL,
            password=settings.FIRST_ADMIN_PASSWORD,
            is_admin=True
        )
        register_user(db, admin_user)

# Call this when starting the app
db = next(get_db())
create_first_admin(db)

@app.get("/")
def root():
    return {"message": "E-Commerce API"}