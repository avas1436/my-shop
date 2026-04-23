import logging
from datetime import datetime, timedelta
from random import random

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import PurposeOTP
from app.config.logging_config import setup_logger
from app.core.security import hashed_password, verify_password
from app.modules.users.models import OTPCode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("otp")


def generate_code(length: int = 5) -> str:
    return "".join(str([random.randint(0, 9) for _ in range(length)]))


def create_otp(
    db: AsyncSession,
    phone_number: str,
    ip_address: str,
    user_agent: str,
    device_id: str,
    purpose: PurposeOTP,
) -> str:
    code = generate_code()

    otp = OTPCode(
        phone_number=phone_number,
        purpose=purpose,
        code_hash=hashed_password(code),
        expires_at=datetime.now(datetime.timezone.utc) + timedelta(minutes=3),
        ip_address=ip_address,
        user_agent=user_agent,
        device_id=device_id,
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)

    return code


logger = setup_logger(Warning)


def verify_otp(
    db: AsyncSession,
    phone: str,
    ip_address: str,
    user_agent: str,
    device_id: str,
    purpose: str,
    code: str,
):
    # جستجوی دیتای کد
    otp = (
        db.query(OTPCode)
        .filter(
            OTPCode.phone_number == phone, OTPCode.purpose == purpose, not OTPCode.used
        )
        .first()
    )

    # بررسی وجود داشتن کد
    if not otp or otp.expires_at < datetime.now(datetime.timezone.utc):
        logger.warning(f"OTP not found for phone={phone}, purpose={purpose}")

        return False

    # بررسی اعتبار داشتن کد
    if not otp or otp.expires_at < datetime.now(datetime.timezone.utc):
        logger.warning(f"OTP expired for phone={phone}")

        return False

    # بررسی device_id
    if otp.device_id != device_id:
        logger.error(
            f"Device mismatch: expected={otp.device_id}, got={device_id}, phone={phone}"
        )

        return False

    # بررسی تغییرات مشکوک IP و UA
    if otp.ip_address != ip_address:
        logger.warning(
            f"IP mismatch (soft): expected={otp.ip_address}, got={ip_address}"
        )

    # بررسی مرورگر
    if otp.user_agent != user_agent:
        logger.warning(
            f"UA mismatch (soft): expected={otp.user_agent}, got={user_agent}"
        )

    # بررسی صحیح بودن کد
    if not verify_password(code, otp.code_hash):
        otp.attempt_count += 1
        db.commit()

        logger.warning(f"Wrong OTP code for {phone} (attempt={otp.attempt_count})")

        return False

    otp.used = True
    otp.used_at = datetime.now(datetime.timezone.utc)
    db.commit()

    logger.info(f"OTP verified for phone={phone}")
    return True
