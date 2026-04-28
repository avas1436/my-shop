from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import PurposeOTP
from app.config.settings import get_settings
from app.core.otp_service import create_otp, verify_otp
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_token_payload,
    hash_password,
    is_refresh_token_active,
    revoke_refresh_token,
    store_refresh_token,
    verify_password,
)
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import LoginWithPassword, OTPVerify, Register, TokenPair

settings = get_settings()


# =========================
# Check New User
# =========================
def is_new_user(user: User) -> bool:
    return (
        user.first_name is None
        or user.last_name is None
        or user.hashed_password is None
    )


# =========================
# Refresh Flow
# =========================
async def issue_token_pair(user: User, redis_client: Redis | None) -> TokenPair:

    access_token = create_access_token(subject=user.phone_number)

    refresh_token = create_refresh_token(subject=user.phone_number)

    refresh_payload = get_token_payload(refresh_token, expected_type="refresh")

    await store_refresh_token(
        redis_client=redis_client,
        token_id=str(refresh_payload["jti"]),
        subject=user.phone_number,
    )

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# ==============================================================================
# Register User or Login
# ==============================================================================
async def request_otp_service(
    db: AsyncSession,
    phone_number: str,
    purpose: PurposeOTP,
    ip_address: str,
    user_agent: str,
    device_id: str,
):
    repo = UserRepository(db)
    user = await repo.get_by_phone(phone_number=phone_number)

    if user and purpose == PurposeOTP.REGISTER:
        raise HTTPException(status_code=400, detail="این شماره قبلاً ثبت‌نام شده است")

    if not user and purpose in (PurposeOTP.LOGIN, PurposeOTP.RESET):
        raise HTTPException(status_code=400, detail="کاربر یافت نشد")

    try:
        code, wait = await create_otp(
            db=db,
            phone_number=phone_number,
            ip_address=ip_address,
            user_agent=user_agent,
            device_id=device_id,
            purpose=purpose,
        )

        if wait:
            await repo.rollback()
            return None, wait

        await repo.commit()

        return code, wait  # در صورت داشتن مقدار برای ویت کدی داده نمیشود

    except Exception:
        await repo.rollback()
        raise


# ==============================================================================
# verify OTP Code - Login with OTP Code
# ==============================================================================
async def verify_otp_service(
    db: AsyncSession,
    data: OTPVerify,
    ip_address: str,
    user_agent: str,
    device_id: str,
    redis_client: Redis | None = None,
) -> TokenPair:
    is_valid = await verify_otp(
        db=db,
        phone=data.phone_number,
        ip_address=ip_address,
        user_agent=user_agent,
        device_id=device_id,
        purpose=data.purpose,
        code=data.code,
    )
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    repo = UserRepository(db)
    user = await repo.get_by_phone(phone_number=data.phone_number)

    if data.purpose == PurposeOTP.REGISTER and user is not None:
        raise HTTPException(status_code=400, detail="این شماره قبلاً ثبت‌نام شده است")

    if data.purpose in (PurposeOTP.LOGIN, PurposeOTP.RESET) and user is None:
        raise HTTPException(status_code=400, detail="کاربر یافت نشد")

    if not user:
        user = await repo.create_user(phone_number=data.phone_number)
        await repo.commit()
        await repo.refresh(user)
    else:
        changed = repo.mark_verified(user=user) and repo.update_login(user=user)
        if changed:
            await repo.commit()

    return await issue_token_pair(user=user, redis_client=redis_client)


# ==============================================================================
# Login with password
# ==============================================================================
async def login_with_password_service(
    db: AsyncSession,
    data: LoginWithPassword,
    redis_client: Redis | None = None,
) -> TokenPair:
    repo = UserRepository(db)
    user = await repo.get_by_phone(phone_number=data.phone_number)

    if not user or not user.hashed_password:
        raise HTTPException(status_code=400, detail="User Not Found")

    if not verify_password(
        password=data.password,
        hashed_password=user.hashed_password,
    ):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    update = repo.update_login(user=user)
    if not update:
        raise HTTPException(status_code=500, detail="Failed to update last login")

    await repo.commit()

    return await issue_token_pair(user=user, redis_client=redis_client)


# ==============================================================================
# Complete Register for new users
# ==============================================================================
async def complete_register_service(
    db: AsyncSession,
    current_user: User,
    data: Register,
) -> User:
    if not is_new_user(current_user):
        raise HTTPException(status_code=400, detail="Profile already completed")

    repo = UserRepository(db)
    hashed = hash_password(password=data.password.get_secret_value())

    try:
        await repo.complete_profile(
            user=current_user,
            first_name=data.first_name,
            last_name=data.last_name,
            birth_date=data.birth_date,
            hashed_password=hashed,
        )
        await repo.commit()
        await repo.refresh(current_user)
        return current_user
    except Exception:
        await repo.rollback()
        raise


async def refresh_token_service(
    db: AsyncSession,
    refresh_token: str,
    redis_client: Redis | None = None,
) -> TokenPair:
    try:
        payload = get_token_payload(refresh_token, expected_type="refresh")
        subject = str(payload["sub"])
        token_id = str(payload["jti"])
    except (ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        ) from None

    is_active = await is_refresh_token_active(
        redis_client=redis_client,
        token_id=token_id,
        subject=subject,
    )
    if not is_active:
        raise HTTPException(
            status_code=401, detail="Refresh token is invalid or revoked"
        )

    repo = UserRepository(db)
    user = await repo.get_by_phone(phone_number=subject)

    if not user or not user.is_active or user.deleted_at is not None:
        await revoke_refresh_token(redis_client=redis_client, token_id=token_id)
        raise HTTPException(status_code=401, detail="User not found or inactive")

    await revoke_refresh_token(redis_client=redis_client, token_id=token_id)
    return await issue_token_pair(user=user, redis_client=redis_client)


# ==============================================================================
# Revoke Refresh Token
# ==============================================================================
async def revoke_refresh_token_service(
    refresh_token: str,
    redis_client: Redis | None = None,
) -> None:
    try:
        payload = get_token_payload(refresh_token, expected_type="refresh")
        token_id = str(payload["jti"])
    except (ValueError, KeyError, TypeError):
        return

    await revoke_refresh_token(redis_client=redis_client, token_id=token_id)


# ==============================================================================
# Revoke All of Active Refresh Tokens
# ==============================================================================
async def revoke_all_refresh_tokens_for_subject_service(
    redis_client: Redis | None,
    subject: str,
) -> None:
    if redis_client is None:
        return

    # فرض: کلیدها با session_prefix:refresh:* ذخیره می‌شن
    # و مقدار هر کلید subject (شماره موبایل) است

    prefix = settings.session_prefix
    pattern = f"{prefix}:refresh:*"
    cursor = 0
    while True:
        cursor, keys = await redis_client.scan(cursor=cursor, match=pattern, count=200)
        if keys:
            values = await redis_client.mget(keys)
            delete_keys = []
            for key, val in zip(keys, values, strict=False):
                if val == subject:
                    delete_keys.append(key)
            if delete_keys:
                await redis_client.delete(*delete_keys)
        if cursor == 0:
            break
