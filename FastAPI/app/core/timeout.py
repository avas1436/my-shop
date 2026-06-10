# app/core/timeout.py

import asyncio

from fastapi import Request

from app.common.responses import create_raw_json_response
from app.config.settings import get_settings

settings = get_settings()


# ---------- Middleware 0: Timeout Middleware ----------
async def request_timeout_middleware(request: Request, call_next):
    if request.url.path in settings.public_path or request.url.path.startswith("/docs"):
        return await call_next(request)

    try:
        # استفاده از ساختار مدرن asyncio.timeout در پایتون 3.12
        async with asyncio.timeout(settings.timeout_duration_seconds):
            return await call_next(request)

    except TimeoutError:
        # خطای TimeoutError داخلی پایتون 3.12 به طور خودکار اینجا کپچر می‌شود
        return create_raw_json_response(
            status_code=504,
            detail={
                "message": "Gateway Timeout",
                "code": "REQUEST_TIMEOUT",
                "detail": f"Request execution exceeded the {settings.timeout_duration_seconds} second limit.",
            },
            error_type="TIMEOUT",
            path=request.url.path,
        )
