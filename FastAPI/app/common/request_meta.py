# app/common/request_meta.py
import ipaddress

from fastapi import Request
from pydantic import BaseModel, Field


class ClientMeta(BaseModel):
    ip: str = Field(..., description="IP واقعی کلاینت (پشت proxy)")
    user_agent: str = Field(..., description="User-Agent کلاینت")
    device_id: str = Field(..., description="Device-ID سفارشی از هدر")
    forwarded_for: str | None = Field(None, description="مقدار خام X-Forwarded-For")


def client_meta(request: Request) -> ClientMeta:
    return ClientMeta(
        ip=extract_real_ip(request),
        user_agent=request.headers.get("user-agent", "unknown"),
        device_id=request.headers.get("device-id", "unknown"),
        forwarded_for=request.headers.get("x-forwarded-for"),
    )


# روش استفاده
# meta: Annotated[ClientMeta, Depends(client_meta)]


def extract_real_ip(request: Request) -> str:

    # لیست رنج‌های IP خصوصی برای فیلتر کردن
    PRIVATE_RANGES = (
        "10.",
        "172.16.",
        "172.17.",
        "172.18.",
        "172.19.",
        "172.20.",
        "172.21.",
        "172.22.",
        "172.23.",
        "172.24.",
        "172.25.",
        "172.26.",
        "172.27.",
        "172.28.",
        "172.29.",
        "172.30.",
        "172.31.",
        "192.168.",
        "127.",
        "::1",
        "fe80:",
    )

    # این تابع بررسی میکند که آی پی پرایوت هست یا نه
    def is_private_ip(ip: str) -> bool:
        try:
            return ipaddress.ip_address(ip).is_private
        except ValueError:
            return True

    # 1. بررسی X-Forwarded-For (فرمت: "client, proxy1, proxy2")
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        # استخراج اولین IP (کلاینت اصلی)
        first_ip = forwarded_for.split(",")[0].strip()
        # فقط اگر IP خصوصی نباشد، آن را برمی‌گردانیم
        if first_ip and not is_private_ip(first_ip):
            return first_ip

    # 2. بررسی X-Real-IP (جایگزین استاندارد)
    real_ip = request.headers.get("x-real-ip")
    if real_ip and not is_private_ip(real_ip.strip()):
        return real_ip.strip()

    # 3. Fallback به IP مستقیم اتصال (برای تست لوکال)
    if request.client and request.client.host:
        return request.client.host

    return "unknown"
