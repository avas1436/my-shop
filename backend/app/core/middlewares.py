import time

from fastapi import FastAPI, Request


def register_middlewares(app: FastAPI) -> None:
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.5f}"
        return response
