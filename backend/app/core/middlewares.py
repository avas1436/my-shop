import asyncio
import time

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator  # prometheus
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address


def register_middlewares(app: FastAPI, trusted_host: list[str]) -> None:

    # Security Middlewares
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_host)

    # Rate‑Limit
    limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # Time-out
    @app.middleware("http")
    async def timeout(request: Request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=10)

        except TimeoutError:
            return JSONResponse({"detail": "Request Timeout"}, status_code=504)

    # ZIP Data - GZIP
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Process Time
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.5f}"
        return response

    # Prometheus Metrics
    Instrumentator().instrument(app).expose(app)
