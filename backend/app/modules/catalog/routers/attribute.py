from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.pagination import PageResponse
from app.modules.catalog.dependencies.attribute import (
    get_attribute_service,
    get_product_attribute_service,
    get_product_variant_attribute_service,
)
from app.modules.catalog.schemas.attribute import (
    AttributeCreate,
    AttributeRead,
    AttributeUpdate,
    ProductAttributeCreate,
    ProductAttributeRead,
    ProductAttributeUpdate,
    ProductVariantAttributeCreate,
    ProductVariantAttributeRead,
    ProductVariantAttributeUpdate,
)
from app.modules.catalog.services.attribute import (
    AttributeService,
    ProductAttributeService,
    ProductVariantAttributeService,
)
from app.modules.users.models import User

router = APIRouter()


# --------------------------------------------------
# Attribure Model
# --------------------------------------------------
@router.post("/", response_model=AttributeRead)
async def create_attribute(
    data: AttributeCreate,
    service: Annotated[AttributeService, Depends(get_attribute_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):
    return await service.create_attribute(data)


@router.get("/{attribute_id}", response_model=AttributeRead)
async def get_attribute(
    attribute_id: int,
    service: Annotated[AttributeService, Depends(get_attribute_service)],
):
    return await service.get_attribute(attribute_id)


@router.get("/list", response_model=PageResponse[dict])
async def list_attributes(
    service: Annotated[AttributeService, Depends(get_attribute_service)],
    search: str | None = None,
    attribute_id: int | None = None,
    page: int = 1,
    size: int = 10,
):
    return await service.list_attributes(search, attribute_id, page, size)


@router.put("/{attribute_id}", response_model=AttributeRead)
async def update_attribute(
    attribute_id: int,
    data: AttributeUpdate,
    service: Annotated[AttributeService, Depends(get_attribute_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):
    return await service.update_attribute(attribute_id, data)


@router.delete("/{attribute_id}")
async def delete_attribute(
    attribute_id: int,
    service: Annotated[AttributeService, Depends(get_attribute_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):

    await service.delete_attribute(attribute_id)

    return {"detail": "Attribute deleted successfully."}


# --------------------------------------------------
# Product Attribure Model
# --------------------------------------------------
@router.post("/product", response_model=ProductAttributeRead)
async def create_product_attribute(
    data: ProductAttributeCreate,
    service: Annotated[ProductAttributeService, Depends(get_product_attribute_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):
    return await service.create_product_attribute(data)


@router.get("/product/{pa_id}", response_model=ProductAttributeRead)
async def get_product_attribute(
    pa_id: int,
    service: Annotated[ProductAttributeService, Depends(get_product_attribute_service)],
):
    return await service.get_product_attribute(pa_id)


@router.get("/list/product/list", response_model=PageResponse[dict])
async def list_product_attributes(
    service: Annotated[ProductAttributeService, Depends(get_product_attribute_service)],
    search: str | None = None,
    product_id: int | None = None,
    attribute_id: int | None = None,
    page: int = 1,
    size: int = 10,
):
    return await service.list_product_attributes(
        search, product_id, attribute_id, page, size
    )


@router.put("/product/{pa_id}", response_model=ProductAttributeRead)
async def update_product_attribute(
    pa_id: int,
    data: ProductAttributeUpdate,
    service: Annotated[ProductAttributeService, Depends(get_product_attribute_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):
    return await service.update_product_attribute(pa_id, data)


@router.delete("/product/{pa_id}")
async def delete_product_attribute(
    pa_id: int,
    service: Annotated[ProductAttributeService, Depends(get_product_attribute_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):

    await service.delete_product_attribute(pa_id)

    return {"detail": "Product attribute deleted successfully."}


# --------------------------------------------------
# Product Variant Attribure Model
# --------------------------------------------------
@router.post("/product/variant", response_model=ProductVariantAttributeRead)
async def create_product_variant_attribute(
    data: ProductVariantAttributeCreate,
    service: Annotated[
        ProductVariantAttributeService, Depends(get_product_variant_attribute_service)
    ],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):
    return await service.create_product_variant_attribute(data)


@router.get("/product/variant/{pva_id}", response_model=ProductVariantAttributeRead)
async def get_product_variant_attribute(
    pva_id: int,
    service: Annotated[
        ProductVariantAttributeService, Depends(get_product_variant_attribute_service)
    ],
):
    return await service.get_product_variant_attribute(pva_id)


@router.get("/list/product/variant", response_model=PageResponse[dict])
async def list_product_variant_attributes(
    service: Annotated[
        ProductVariantAttributeService, Depends(get_product_variant_attribute_service)
    ],
    search: str | None = None,
    variant_id: int | None = None,
    attribute_id: int | None = None,
    page: int = 1,
    size: int = 10,
):

    return await service.list_product_variant_attributes(
        search, variant_id, attribute_id, page, size
    )


@router.put("/product/variant/{pva_id}", response_model=ProductVariantAttributeRead)
async def update_product_variant_attribute(
    pva_id: int,
    data: ProductVariantAttributeUpdate,
    service: Annotated[
        ProductVariantAttributeService, Depends(get_product_variant_attribute_service)
    ],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):
    return await service.update_product_variant_attribute(pva_id, data)


@router.delete("/product/variant/{pva_id}")
async def delete_product_variant_attribute(
    pva_id: int,
    service: Annotated[
        ProductVariantAttributeService, Depends(get_product_variant_attribute_service)
    ],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):

    await service.delete_product_variant_attribute(pva_id)

    return {"detail": "Variant attribute deleted successfully."}
