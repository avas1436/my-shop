import re
import time
from typing import Any

from app.core.slowapi_storage import RedisAsyncStorage
from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

#  ---------- الگوهای Bot Detection ----------
SUSPICIOUS_UA_RE = re.compile(
    r"(python-requests|go-http-client|sqlmap|nikto|masscan|zgrab|nmap|scrapy)",
    re.IGNORECASE,
)

PUBLIC_PATHS = {"/health", "/metrics", "/docs", "/openapi.json", "/redoc"}

# ---------- Rate Limiter ----------
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],
    strategy="fixed-window",
)


def _error_response(
    status_code: int,
    message: str,
    code: str | None = None,
    details: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    content: dict[str, Any] = {
        "message": message,
        "code": code,
        "details": details,
    }
    return JSONResponse(status_code=status_code, content=content, headers=headers)


# ---------- Middleware 1: Block Suspicious Bots ----------
async def block_suspicious_bots(request: Request, call_next):
    """بلاک کردن ربات‌های مخرب قبل از Rate Limit."""
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    user_agent = request.headers.get("user-agent", "")

    if SUSPICIOUS_UA_RE.search(user_agent):
        return _error_response(
            status_code=403,
            message="Forbidden",
            code="SUSPICIOUS_BOT",
            headers={"X-Blocked-Reason": "suspicious-bot"},
        )

    x_forwarded = request.headers.get("x-forwarded-for", "")

    if x_forwarded and len(x_forwarded.split(",")) > 5:
        return _error_response(
            status_code=400,
            message="Bad Request",
            code="INVALID_FORWARDED_HEADER",
        )

    return await call_next(request)


# ---------- Middleware 2: Process Time ----------
async def add_process_time(request: Request, call_next):
    """محاسبه زمان پردازش برای monitoring."""
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
    return response


# ---------- ثبت Middlewares ----------
def register_middlewares(app: FastAPI, trusted_host: list[str]) -> None:
    # 1. Process Time
    app.middleware("http")(add_process_time)

    # 2. Rate Limiter با Redis از app.state
    redis_controller = getattr(app.state, "redis", None)
    if redis_controller and redis_controller.redis_client:
        limiter._storage = RedisAsyncStorage(
            redis_client=redis_controller.redis_client,
            prefix="ratelimit:",
            expiration=60,
        )
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # 3. Trusted Host
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_host)

    # 4. Bot Blocking (اولین لایه دفاع)
    app.middleware("http")(block_suspicious_bots)

    # ---------- Rate Limit Handler ----------
    @app.exception_handler(RateLimitExceeded)
    async def handle_rate_limit(request: Request, exc: RateLimitExceeded):
        retry_after = str(exc.detail)
        return _error_response(
            status_code=429,
            message="Too Many Requests",
            code="RATE_LIMIT_EXCEEDED",
            details={
                "retry_after": int(retry_after)
                if retry_after.isdigit()
                else retry_after,
                "endpoint": request.url.path,
            },
            headers={"Retry-After": retry_after},
        )

    # 5. Prometheus Metrics
    Instrumentator().instrument(app)  # .expose(app)
