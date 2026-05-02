# app/common/responses.py
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from fastapi import Request
from fastapi.responses import JSONResponse, Response
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
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


def success_payload(
    *,
    data: Any,
    path: str,
    status_code: int = 200,
    message: str = "ok",
    code: str | None = None,
    meta: dict[str, Any] | None = None,
) -> SuccessResponse:

    return SuccessResponse(
        status_code=status_code,
        message=message,
        code=code,
        data=data,
        meta=meta,
        path=path,
        timestamp=datetime.now(UTC).isoformat(),
    )


# ---------- Error ----------
class ErrorResponse(BaseModel):
    success: bool = False
    status_code: int
    error_type: str
    detail: Any
    path: str
    timestamp: str


def error_payload(
    *,
    status_code: int,
    detail: Any,
    error_type: str,
    path: str,
):
    return ErrorResponse(
        status_code=status_code,
        error_type=error_type,
        detail=detail,
        path=path,
        timestamp=datetime.now(UTC).isoformat(),
    )


# ---------- Auto Wrapper for Success ----------
class SuccessAPIRoute(APIRoute):
    def get_route_handler(self):
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request):
            result = await original_handler(request)

            # اگر Response برگردونی (FileResponse و ...)
            if isinstance(result, Response):
                return result

            # پیام سفارشی متنی
            if isinstance(result, SuccessMessage):
                status_code = self.status_code or 200
                payload = success_payload(
                    data=None,
                    message=result.message,
                    status_code=status_code,
                    path=request.url.path,
                )
                return JSONResponse(payload.model_dump(), status_code=status_code)

            status_code = self.status_code or 200
            payload = success_payload(
                data=result,
                path=request.url.path,
                status_code=status_code,
            )
            return JSONResponse(payload.model_dump(), status_code=status_code)

        return custom_handler
