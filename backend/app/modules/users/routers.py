from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from kavenegar import APIException, HTTPException as KHTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import PurposeOTP
from app.core.database import get_db
from app.core.otp_service import create_otp
from app.core.sms_service import send_sms
from app.modules.users.schemas import RequestOTP

router = APIRouter()


@router.post(
    "/otp/request",
    status_code=status.HTTP_201_CREATED,
)
async def request_otp(
    request: Request,
    data: RequestOTP,
    purpose: PurposeOTP,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    device_id = request.headers.get("device-id", "unknown")

    try:
        code, wait = await create_otp(
            db=db,
            phone_number=data.phone_number,
            ip_address=ip,
            user_agent=user_agent,
            device_id=device_id,
            purpose=purpose,
        )

        if wait:
            raise HTTPException(
                status_code=429,
                detail=f"please wait for {wait} seconds",
            )

        # ارسال پیامک به صورت async
        await send_sms(
            receptor=data.phone_number,
            code=code,
        )

        return {"message": "OTP sent successfully"}

    except APIException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from None

    except KHTTPException as e:
        raise HTTPException(
            status_code=502,
            detail=str(e),
        ) from None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from None


# @router.post("/login", response_model=TokenPair)
# async def login_user(
#     payload: LoginRequest, db: AsyncSession = Depends(get_db_session)
# ) -> TokenPair:
#     service = UserService(UserRepository(db))
#     return await service.login(payload)


# @router.get("/me")
# async def read_current_user(
#     user_id: int = Depends(get_current_user_id),
# ) -> dict[str, int]:
#     return {"user_id": user_id}
