import cloudinary
import cloudinary.uploader
from core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

def upload_profile_image(file, user_id: str):
    """Uploads image to Cloudinary's profile folder"""
    result = cloudinary.uploader.upload(
        file,
        folder=f"profile_images",
        public_id=f"user_{user_id}", 
        overwrite=True,  
        allowed_formats=["jpg", "png", "jpeg"],
        transformation=[
            {"width": 500, "height": 500, "crop": "fill"},
            {"quality": "auto"}
        ]
    )
    return result["secure_url"]

async def upload_product_image(file, product_id: int):
    """Upload image to Cloudinary's products folder"""
    result = cloudinary.uploader.upload(
        file,
        folder="products",
        public_id=f"product_{product_id}",  
        overwrite=True  
    )
    return result["secure_url"]

def delete_product_image(product_id: int):
    """Delete image from Cloudinary's products folder"""
    public_id = f"products/product_{product_id}"
    cloudinary.uploader.destroy(public_id)