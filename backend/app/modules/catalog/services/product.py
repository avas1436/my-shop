from app.cache.product_cache import ProductCache
from app.modules.catalog.models.product import Product
from app.modules.catalog.repository.product import AdminProductRepository
from app.modules.catalog.schemas.product import DraftProductCreate


class AdminProductService:
    def __init__(
        self,
        repository: AdminProductRepository,
        cache: ProductCache | None = None,
    ):
        self.repository = repository
        self.cache = cache

    async def draft_create(self, payload: DraftProductCreate) -> Product:
        product = Product(
            name=payload.name,
            slug=payload.slug,
            description=payload.description,
            price=payload.price,
            cost_price=payload.cost_price,
            tax_rate=payload.tax_rate,
            status=payload.status,
            is_featured=payload.is_featured,
            is_digital=payload.is_digital,
            weight=payload.weight,
            meta_title=payload.meta_title,
            meta_description=payload.meta_description,
            gtin=payload.gtin,
        )
        created = await self.repository.create(product)
        if self.cache:
            await self.cache.set_product(
                created.id,
                {
                    "id": created.id,
                    "name": created.name,
                    "price": created.price,
                },
            )
        return created

    async def list_all(self) -> list[Product]:
        return await self.repository.list_all()

    async def get_by_id(self, product_id: int) -> Product | dict | None:
        if self.cache:
            cached = await self.cache.get_product(product_id)
            if cached:
                return cached
        return await self.repository.get_by_id(product_id)
