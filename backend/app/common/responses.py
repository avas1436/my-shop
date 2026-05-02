# app/common/responses.py
import json
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from fastapi import Request
from fastapi.responses import Response
from fastapi.routing import APIRoute
from pydantic import BaseModel, Field

T = TypeVar("T")


# برای دادن خروجی متنی
class SuccessMessage(BaseModel):
    message: str


# ---------- Success ----------
class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    status_code: int
    message: str = "ok"
    code: str | None = None
    data: T
    meta: dict[str, Any] | None = None
    path: str
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


def success_payload(
    *,
    data: Any,
    path: str,
    status_code: int = 200,
    message: str = "ok",
    code: str | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:

    now = datetime.now(UTC)

    return {
        "success": True,
        "status_code": status_code,
        "message": message,
        "code": code,
        "data": data,
        "meta": meta,
        "path": path,
        "timestamp": now.isoformat(),
    }


# ---------- Error ----------
class ErrorResponse(BaseModel):
    success: bool = False
    status_code: int
    error_type: str
    detail: Any
    path: str
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


def error_payload(
    *,
    status_code: int,
    detail: Any,
    error_type: str,
    path: str,
) -> dict[str, Any]:

    now = datetime.now(UTC)

    return {
        "success": False,
        "status_code": status_code,
        "error_type": error_type,
        "detail": detail,
        "path": path,
        "timestamp": now.isoformat(),
    }


# ---------- Auto Wrapper for Success ----------
class SuccessAPIRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request) -> Response:
            # اجرای handler اصلی
            response = await original_handler(request)

            # اگر response از نوع Response است، body را بخوانید
            if isinstance(response, Response):
                # خواندن body
                body_bytes = response.body

                try:
                    body = json.loads(body_bytes)
                except (json.JSONDecodeError, ValueError):
                    # اگر JSON نیست، همان response را برگردانید
                    return response

                # اگر قبلاً wrap شده، برگردانید
                if isinstance(body, dict) and "success" in body:
                    return response

                # wrap کردن data
                status_code = response.status_code
                wrapped = success_payload(
                    data=body,
                    path=str(request.url.path),
                    status_code=status_code,
                )

                new_body_bytes = json.dumps(wrapped, separators=(",", ":")).encode(
                    "utf-8"
                )
                response.body = new_body_bytes
                response.headers["content-length"] = str(len(new_body_bytes))
                return response

            return response

        return custom_handler
