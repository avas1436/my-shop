# catalog
from app.modules.catalog.models.attribute import (
    Attribute,
    ProductAttribute,
    ProductVariantAttribute,
)
from app.modules.catalog.models.brand import Brand
from app.modules.catalog.models.category import Category, ProductCategory
from app.modules.catalog.models.image import ProductImage

# inventory
from app.modules.catalog.models.inventory import Inventory
from app.modules.catalog.models.product import Product
from app.modules.catalog.models.tag import ProductTag, Tag
from app.modules.catalog.models.variant import ProductVariant

# comments
from app.modules.comments.models import Comment

# users
from app.modules.users.models import User
