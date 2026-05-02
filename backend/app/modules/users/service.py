from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.common.enums import PurposeOTP
from app.common.request_meta import ClientMeta
from app.config.settings import get_settings
from app.core.otp_service import create_otp, verify_otp
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_token_payload,
    hash_password,
    verify_password,
)
from app.errors.errors import (
    BadRequest,
    Conflict,
    HttpError,
    InternalServerError,
    Unauthorized,
)
from app.modules.users.models import User
from app.modules.users.schemas import (
    LoginWithPassword,
    OTPVerify,
    Register,
    RequestOTP,
    TokenPair,
)

settings = get_settings()


# =========================
# Check New User
# =========================
# def is_new_user(user: User) -> bool:
#     return (
#         user.first_name is None
#         or user.last_name is None
#         or user.hashed_password is None
#     )


# =========================
# Refresh Flow
# =========================
async def issue_token_pair(user: User, cache: RedisCache) -> TokenPair:

    access_token = create_access_token(subject=user.phone_number)

    refresh_token = create_refresh_token(subject=user.phone_number)

    refresh_payload = get_token_payload(refresh_token, expected_type="refresh")

    await cache.store(
        jti=str(refresh_payload["jti"]),
        subject=str(refresh_payload["sub"]),
    )

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )


class AuthService:
    def __init__(self, db: AsyncSession, cache: RedisCache, meta: ClientMeta):
        self.repo = db
        self.cache = cache
        self.meta = meta

    # ============================================
    # Register User or Login
    # ============================================
    async def request_otp_service(
        self,
        data: RequestOTP,
    ):

        user = await self.repo.get_by_phone(phone_number=data.phone_number)

        if user and data.purpose == PurposeOTP.REGISTER:
            raise BadRequest("User with this phone number already registered.")

        if not user and data.purpose in (PurposeOTP.LOGIN, PurposeOTP.RESET):
            raise BadRequest("User not found")

        try:
            code, wait = await create_otp(
                db=self.repo,
                phone_number=data.phone_number,
                ip_address=self.meta.ip,
                user_agent=self.meta.user_agent,
                device_id=self.meta.device_id,
                purpose=data.purpose,
            )

            if wait:
                await self.repo.rollback()
                return None, wait

            await self.repo.commit()

            return code, wait  # در صورت داشتن مقدار برای ویت کدی داده نمیشود

        except HttpError:
            await self.repo.rollback()
            raise

        except IntegrityError:
            await self.repo.rollback()
            raise Conflict("Duplicate OTP or user state conflict") from None

        except Exception:
            await self.repo.rollback()
            raise InternalServerError("Unexpected error") from None

    # ============================================
    # verify OTP Code - Login with OTP Code
    # ============================================
    async def verify_otp_service(
        self,
        data: OTPVerify,
    ) -> TokenPair:

        is_valid = await verify_otp(
            db=self.repo,
            phone=data.phone_number,
            ip_address=self.meta.ip,
            user_agent=self.meta.user_agent,
            device_id=self.meta.device_id,
            purpose=data.purpose,
            code=data.code,
        )

        if not is_valid:
            raise BadRequest("Invalid or expired OTP")

        user = await self.repo.get_by_phone(phone_number=data.phone_number)

        if data.purpose == PurposeOTP.REGISTER and user is not None:
            raise BadRequest("User with this phone number already registered.")

        if data.purpose in (PurposeOTP.LOGIN, PurposeOTP.RESET) and user is None:
            raise BadRequest("User not found.")

        if not user:
            user = await self.repo.create_user(phone_number=data.phone_number)
            await self.repo.commit()
            await self.repo.refresh(user)
        else:
            changed = self.repo.mark_verified(user=user) and self.repo.update_login(
                user=user
            )

            if changed:
                await self.repo.commit()

        return await issue_token_pair(user=user, cache=self.cache)

    # ============================================
    # Login with password
    # ============================================
    async def login_with_password_service(
        self,
        data: LoginWithPassword,
    ) -> TokenPair:

        user = await self.repo.get_by_phone(phone_number=data.phone_number)

        if not user or not user.hashed_password:
            raise BadRequest("User not found.")

        if not verify_password(
            password=data.password,
            hashed_password=user.hashed_password,
        ):
            raise BadRequest("Invalid credentials")

        update = self.repo.update_login(user=user)
        if not update:
            raise InternalServerError("Failed to update last login")

        await self.repo.commit()

        return await issue_token_pair(user=user, cache=self.cache)

    # ============================================
    # Complete Register for new users
    # ============================================
    async def complete_register_service(
        self,
        data: Register,
        current_user: User,
    ) -> User:

        if not (
            current_user.first_name is None
            or current_user.last_name is None
            or current_user.hashed_password is None
        ):
            raise BadRequest("Profile already completed")

        hashed = hash_password(password=data.password.get_secret_value())

        try:
            await self.repo.complete_profile(
                user=current_user,
                first_name=data.first_name,
                last_name=data.last_name,
                birth_date=data.birth_date,
                hashed_password=hashed,
            )
            await self.repo.commit()
            await self.repo.refresh(current_user)
            return current_user

        except HttpError:
            await self.repo.rollback()
            raise

        except Exception:
            await self.repo.rollback()
            raise InternalServerError("Unexpected error") from None

    # ============================================
    # Refresh Token Service
    # ============================================
    async def refresh_token_service(
        self,
        refresh_token: str,
    ) -> TokenPair:

        payload = get_token_payload(refresh_token, expected_type="refresh")
        subject = str(payload["sub"])
        token_id = str(payload["jti"])

        is_active = await self.cache.is_active(
            jti=token_id,
            subject=subject,
        )
        if not is_active:
            raise Unauthorized("Refresh token is invalid or revoked")

        user = await self.repo.get_by_phone(phone_number=subject)

        if not user or not user.is_active or user.deleted_at is not None:
            await self.cache.revoke(jti=token_id, subject=subject)
            raise Unauthorized("User not found or inactive")

        await self.cache.revoke(jti=token_id, subject=subject)
        return await issue_token_pair(user=user, cache=self.cache)

    # ============================================
    # Revoke Refresh Token
    # ============================================
    async def revoke_refresh_token_service(
        self,
        refresh_token: str,
    ) -> None:

        payload = get_token_payload(refresh_token, expected_type="refresh")
        token_id = str(payload["jti"])
        subject = str(payload["sub"])

        await self.cache.revoke(jti=token_id, subject=subject)

    # ============================================
    # Revoke All of Active Refresh Tokens
    # ============================================
    async def revoke_all_refresh_tokens_for_subject_service(
        self,
        phone_number: str,
    ) -> None:

        await self.cache.revoke(phone_number=phone_number)
