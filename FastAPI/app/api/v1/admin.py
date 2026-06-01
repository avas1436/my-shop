from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.core.middlewares import limiter
from app.modules.users.models import User

router = APIRouter()


AdminOnly = Annotated[
    User,
    Depends(
        require_access(
            allowed_roles=[UserRole.ADMIN],
            deny_roles=[UserRole.CUSTOMER],
            require_recent_login_within=timedelta(days=1),
            require_password=True,
            require_profile_complete=True,
            profile_required_fields=("first_name", "last_name", "birth_date"),
        ),
    ),
]


@router.get("/routes")
@limiter.limit("5/minute")
async def list_all_routes(
    request: Request,
    _: AdminOnly,
):
    routes = []
    for r in request.app.routes:
        methods = sorted(list(getattr(r, "methods", []) or []))
        routes.append(
            {
                "path": getattr(r, "path", None),
                "name": getattr(r, "name", None),
                "methods": methods,
            }
        )
    return {"count": len(routes), "routes": routes}


@router.get("/metrics", response_class=PlainTextResponse)
@limiter.limit("5/day")
async def metrics(
    request: Request,
    _: AdminOnly,
):
    data = generate_latest()
    return PlainTextResponse(
        content=data.decode("utf-8"), media_type=CONTENT_TYPE_LATEST
    )
