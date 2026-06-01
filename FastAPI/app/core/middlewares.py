# app/core/middlewares.py
import re
import time

from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.common.request_meta import extract_real_ip
from app.common.responses import create_raw_json_response
from app.config.settings import get_settings

#  ---------- الگوهای Bot Detection ----------
SUSPICIOUS_UA_RE = re.compile(
    r"(python-requests|go-http-client|sqlmap|nikto|masscan|zgrab|nmap|scrapy)",
    re.IGNORECASE,
)

PUBLIC_PATHS = {"/health", "/metrics", "/docs", "/openapi.json", "/redoc"}


settings = get_settings()


# ---------- Rate Limiter ----------
limiter = Limiter(
    key_func=extract_real_ip,
    default_limits=["100/minute"],
    strategy="fixed-window",
    storage_uri=settings.redis_url,
)


# ---------- Middleware 1: Block Suspicious Bots ----------
async def block_suspicious_bots(request: Request, call_next):

    # مسیرهای عمومی را بررسی نکن
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    user_agent = request.headers.get("user-agent", "")

    # بررسی User-Agent مشکوک
    if SUSPICIOUS_UA_RE.search(user_agent):
        return create_raw_json_response(
            content={
                "message": "Forbidden",
                "code": "SUSPICIOUS_BOT",
                "details": {
                    "user_agent": user_agent[:100],
                    "client_ip": extract_real_ip(request),
                },
            },
            status_code=403,
            headers={"X-Blocked-Reason": "suspicious-bot"},
            include_meta=False,  # بدون meta برای کاهش حجم پاسخ
            path=request.url.path,
        )

    # بررسی header های مشکوک
    x_forwarded = request.headers.get("x-forwarded-for", "")
    if x_forwarded and len(x_forwarded.split(",")) > 5:
        return create_raw_json_response(
            content={
                "message": "Bad Request",
                "code": "INVALID_FORWARDED_HEADER",
                "details": {
                    "x_forwarded_count": len(x_forwarded.split(",")),
                },
            },
            status_code=400,
            include_meta=False,
            path=request.url.path,
        )

    return await call_next(request)


# ---------- Middleware 2: Process Time ----------
async def add_process_time(request: Request, call_next):
    """محاسبه زمان پردازش برای monitoring."""
    # مسیرهای عمومی را نادیده بگیر
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    start = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


# ---------- ثبت Middlewares ----------
def register_middlewares(app: FastAPI, trusted_host: list[str]) -> None:
    # 1. Process Time
    app.middleware("http")(add_process_time)

    # 2. Rate Limiter با Redis از app.state
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

        return create_raw_json_response(
            content={
                "message": "Too Many Requests",
                "code": "RATE_LIMIT_EXCEEDED",
                "details": {
                    "retry_after": int(retry_after)
                    if retry_after.isdigit()
                    else retry_after,
                    "endpoint": request.url.path,
                    "client_ip": extract_real_ip(request),
                },
            },
            status_code=429,
            headers={"Retry-After": retry_after},
            include_meta=True,  # با meta برای ردیابی
            path=request.url.path,
        )

    # 5. Prometheus Metrics
    Instrumentator().instrument(app)  # .expose(app)
