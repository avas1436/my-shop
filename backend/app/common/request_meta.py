# app/common/request_meta.py

from fastapi import Request
from pydantic import BaseModel


class ClientMeta(BaseModel):
    ip: str
    user_agent: str
    device_id: str


def client_meta(request: Request) -> ClientMeta:
    return ClientMeta(
        ip=request.client.host if request.client else "unknown",
        user_agent=request.headers.get("user-agent", "unknown"),
        device_id=request.headers.get("device-id", "unknown"),
    )


# روش استفاده
# meta: Annotated[ClientMeta, Depends(client_meta)]
