# from app.modules.comments.routers import router as comments_router

from fastapi import APIRouter

from app.common.responses import SuccessAPIRoute
from app.modules.catalog.routers.attribute import router as attribute_router
from app.modules.catalog.routers.brand import router as brand_router
from app.modules.catalog.routers.category import router as categories_router
from app.modules.catalog.routers.image import router as images_router
from app.modules.catalog.routers.inventory import router as inventory_router
from app.modules.catalog.routers.product import router as products_router
from app.modules.catalog.routers.tag import router as tag_router
from app.modules.catalog.routers.variant import router as variant_router
from app.modules.users.routers import router as users_router

# با اضافه کردن این قسمت در کل پروژه فرمت پاسخ موفق متحد الشکل می شود
api_router = APIRouter(route_class=SuccessAPIRoute)


api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(images_router, prefix="/images", tags=["images"])
api_router.include_router(brand_router, prefix="/brands", tags=["Brands"])
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
api_router.include_router(tag_router, prefix="/tags", tags=["tags"])
api_router.include_router(attribute_router, prefix="/attributes", tags=["attribute"])
api_router.include_router(variant_router, prefix="/variants", tags=["variant"])
api_router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
# api_router.include_router(comments_router, prefix="/comments", tags=["comments"])
