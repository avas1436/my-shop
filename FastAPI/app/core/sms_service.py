# app/core/sms_service.py
import logging
from typing import Any

from kavenegar import APIException, HTTPException, KavenegarAPI

from app.config.settings import get_settings

settings = get_settings()


logger = logging.getLogger(__name__)


# def send_sms(
#     receptor: str,
#     code: str,
#     api_key: str = settings.kavenegarapi,
# ):

#     api = KavenegarAPI(api_key)

#     params = {
#         "sender": "2000660110",
#         "receptor": receptor,
#         "message": f"کد ورود به سایت الکی ما : {code}",
#     }

#     try:
#         # اجرای تابع همگام در ترد جداگانه
#         response = api.sms_send(params)
#         return response

#     except APIException as e:
#         print(e)
#         raise

#     except HTTPException as e:
#         print(e)
#         raise


def _sms(
    receptor: str,
    message: str,
    sender: str = "2000660110",
    api_key: str | None = None,
) -> dict[str, Any] | None:
    """
    ارسال پیامک عمومی (برای استفاده در پس‌زمینه).
    در صورت موفقیت، result را برمی‌گرداند.
    در صورت خطا، آن را لاگ کرده و None برمی‌گرداند.
    """
    api_key = api_key or settings.kavenegarapi
    api = KavenegarAPI(api_key)

    params = {
        "sender": sender,
        "receptor": receptor,
        "message": message,
    }

    try:
        response = api.sms_send(params)
        logger.info("SMS sent to %s successfully", receptor)
        return response

    except APIException as e:
        logger.error(
            "Kavenegar API error for receptor %s: %s (code=%s)",
            receptor,
            e,
            getattr(e, "code", "unknown"),
        )
        # می‌توانید اینجا بر اساس کد خطا (مثلاً 415 به معنای اتمام سقف) اقدام خاصی کنید
        return None

    except HTTPException as e:
        logger.error(
            "Kavenegar HTTP error for receptor %s: %s (status=%s)",
            receptor,
            e,
            getattr(e, "status_code", "unknown"),
        )
        return None

    except Exception as e:
        logger.critical(
            "Unexpected error sending SMS to %s: %s", receptor, e, exc_info=True
        )
        return None


def send_sms(
    receptor: str,
    code: str,
    api_key: str = settings.kavenegarapi,
) -> dict[str, Any] | None:
    """
    ارسال کد تأیید (طراحی‌شده برای پس‌زمینه).
    نتیجه را برمی‌گرداند (None در صورت شکست) و خطایی raise نمی‌کند.
    """
    message = f"کد ورود به سایت الکی ما : {code}"
    return _sms(
        receptor=receptor,
        message=message,
        api_key=api_key,
    )
