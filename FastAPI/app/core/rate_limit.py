# app/core/rate_limit.py
import time
from types import MappingProxyType  # یک ساختار داده ایمن و سریع و غیر قابل تغییر

from fastapi import Request

from app.common.request_meta import extract_real_ip
from app.common.responses import create_raw_json_response
from app.core.security import get_token_subject

# تعریف ثانیه‌های مربوط به هر بازه زمانی ثابت
TIME_WINDOWS = MappingProxyType(
    {
        "minute": 60,
        "hour": 3600,
        "day": 86400,
        "week": 604800,
    },
)


class ASGIRateLimitMiddleware:
    # تعریف در سطح کلاس به صورت ایمن و فقط‌خواندنی
    STRICT_ROUTES = MappingProxyType(
        {
            "/api/v1/auth/login": MappingProxyType(
                {
                    "user": {
                        "minute": 5,
                        "hour": 20,
                        "day": 100,
                    },
                    "guest": {
                        "minute": 5,
                        "hour": 20,
                        "day": 100,
                    },
                }
            ),
            "/api/v1/admin/infra/routes": MappingProxyType(
                {
                    "user": {
                        "minute": 1,
                        "hour": 20,
                        "day": 100,
                    },
                    "guest": {
                        "minute": 1,
                        "hour": 20,
                        "day": 100,
                    },
                }
            ),
        }
    )

    def __init__(self, app, global_limits=None):
        self.app = app

        # محدودیت‌های عمومی
        self.global_limits = global_limits or {"minute": 60, "hour": 1000}

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # اطلاعات درخواست
        request = Request(scope, receive)

        # آدرس روت
        path = request.url.path

        # آیپی
        client_ip = extract_real_ip(request)

        # شناسه کاربر
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                user_id = get_token_subject(token)
            except Exception:
                # اگر توکن نامعتبر بود، خطا نمی‌دهیم تا لایه
                # در این حالت لیمیت بر اساس آی‌پی اعمال می‌شود.
                pass

        # دریافت کلاینت Redis از State
        try:
            redis_client = request.app.state.redis.RedisController
        except AttributeError:
            redis_client = None

        if not redis_client:
            return await self.app(scope, receive, send)

        # تعیین اینکه محدودیت سخت‌گیرانه است یا عمومی
        is_strict = path in self.STRICT_ROUTES
        limits_to_apply = {}

        if is_strict:
            route_config = self.STRICT_ROUTES[path]
            # بررسی اینکه آیا برای کاربر مهمان و لاگین‌کرده محدودیت مجزا تعریف شده یا خیر
            if user_id and "user" in route_config:
                limits_to_apply = route_config["user"]
            elif not user_id and "guest" in route_config:
                limits_to_apply = route_config["guest"]
            else:
                limits_to_apply = route_config
        else:
            limits_to_apply = self.global_limits

        # ساخت کلیدهای ردیس و اجرای اتمیک با Pipeline
        pipeline = redis_client.pipeline()
        keys_and_limits = []

        for window_name, limit_value in limits_to_apply.items():
            if window_name not in TIME_WINDOWS:
                continue

            window_seconds = TIME_WINDOWS[window_name]
            current_window = int(time.time() // window_seconds)

            # جداسازی (Namespace) بر اساس نوع مسیر و کاربر
            prefix = f"strict:{path}" if is_strict else "global"
            actor = f"user:{user_id}" if user_id else f"ip:{client_ip}"

            redis_key = f"ratelimit:{prefix}:{actor}:{window_name}:{current_window}"

            pipeline.incr(redis_key)
            pipeline.expire(redis_key, window_seconds)

            keys_and_limits.append((redis_key, limit_value))

        try:
            # اجرای تمام دستورات در ردیس به صورت همزمان
            results = await pipeline.execute()

            # بررسی نتایج
            for i, (key, limit) in enumerate(keys_and_limits):
                # دستور incr اولین دستور برای هر کلید در پایپ‌لاین است (ایندکس‌های زوج 0, 2, 4)
                request_count = results[i * 2]

                if request_count > limit:
                    response = create_raw_json_response(
                        status_code=429,
                        detail="تعداد درخواست‌های شما بیش از حد مجاز است.",
                        error_type="TOO_MANY_REQUESTS",
                        path=path,
                        headers={"Retry-After": str(window_seconds)},
                    )
                    await response(scope, receive, send)
                    return
        except Exception:
            # در صورت بروز خطا در ارتباط با ردیس هنگام پردازش لیمیت، درخواست را قطع نمی‌کنیم
            pass

        # عبور به لایه بعدی اپلیکیشن
        await self.app(scope, receive, send)
