import logging
import random
from datetime import UTC, datetime, timedelta

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import PurposeOTP
from app.config.logging_config import setup_logger
from app.config.settings import get_settings
from app.core.security import hash_password, verify_password
from app.modules.users.models import OTPCode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("otp")
settings = get_settings()


def generate_code(length: int = 5) -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(length))


async def create_otp(
    db: AsyncSession,
    phone_number: str,
    ip_address: str,
    user_agent: str,
    device_id: str,
    purpose: PurposeOTP,
) -> tuple[str | None, int | None]:

    code = generate_code()
    now = datetime.now(UTC)
    expires_at = now + timedelta(seconds=settings.otp_ttl)

    async with db.begin():
        # جلوگیری از race برای یک شماره/هدف مشخص
        lock_key = f"otp:{phone_number}:{purpose}"
        await db.execute(
            text("SELECT pg_advisory_xact_lock(hashtext(:k))"),
            {"k": lock_key},
        )

        stmt = (
            select(OTPCode)
            .where(
                OTPCode.phone_number == phone_number,
                OTPCode.purpose == purpose,
                OTPCode.used.is_(False),
            )
            .with_for_update()
        )

        res = await db.execute(stmt)
        otp = res.scalar_one_or_none()

        if otp:
            # rate limit
            if otp.created_at and (now - otp.created_at) < timedelta(
                seconds=settings.otp_cooldown
            ):
                wait = timedelta(seconds=settings.otp_cooldown) - (now - otp.created_at)

                return None, int(wait.total_seconds())

            # تمدید/بازنویسی OTP
            otp.code_hash = hash_password(code)
            otp.expires_at = expires_at
            otp.used = False
            otp.used_at = None
            otp.attempt_count = 0
            otp.ip_address = ip_address
            otp.user_agent = user_agent
            otp.device_id = device_id
            otp.created_at = now
        else:
            db.add(
                OTPCode(
                    phone_number=phone_number,
                    purpose=purpose,
                    code_hash=hash_password(code),
                    expires_at=expires_at,
                    used=False,
                    attempt_count=0,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    device_id=device_id,
                    created_at=now,
                )
            )

    return code, None


logger = setup_logger("Warning")


async def verify_otp(
    db: AsyncSession,
    phone: str,
    ip_address: str,
    user_agent: str,
    device_id: str,
    purpose: str,
    code: str,
):
    # جستجوی دیتای کد
    otp = select(OTPCode).where(
        OTPCode.phone_number == phone,
        OTPCode.purpose == purpose,
        not OTPCode.used,
    )

    # بررسی وجود داشتن کد
    if not otp or otp.expires_at < datetime.now(UTC):
        logger.warning(f"OTP not found for phone={phone}, purpose={purpose}")

        return False

    # بررسی اعتبار داشتن کد
    if not otp or otp.expires_at < datetime.now(UTC):
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
        await db.commit()

        logger.warning(f"Wrong OTP code for {phone} (attempt={otp.attempt_count})")

        return False

    otp.used = True
    otp.used_at = datetime.now(UTC)
    await db.commit()

    logger.info(f"OTP verified for phone={phone}")
    return True
