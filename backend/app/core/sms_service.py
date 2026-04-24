import asyncio

from kavenegar import APIException, HTTPException, KavenegarAPI

from app.config.settings import get_settings

settings = get_settings()


async def send_sms(
    receptor: str,
    code: str,
    api_key: str = settings.kavenegarapi,
):

    api = KavenegarAPI(api_key)

    params = {
        "sender": "2000660110",
        "receptor": receptor,
        "message": f"کد ورود به سایت الکی ما : {code}",
    }

    try:
        # اجرای تابع همگام در ترد جداگانه
        response = await asyncio.to_thread(api.sms_send, params)
        return response

    except APIException as e:
        print(e)
        raise

    except HTTPException as e:
        print(e)
        raise
