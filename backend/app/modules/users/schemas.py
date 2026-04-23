from backend.app.modules.users.utils import validate_phone
from pydantic import BaseModel, Field, field_validator

from app.common.enums import PurposeOTP, UserRole


# ==============================================================================
# Register User and Login
# ==============================================================================
class RequestOTP(BaseModel):
    phone_number: str
    purpose: PurposeOTP = Field(default=PurposeOTP.LOGIN) # LOGIN | REGISTER | RESET

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str):
        return validate_phone(phone_number=v)


# ==============================================================================
# Input OTP Code
# ==============================================================================
class OTPCode(BaseModel):
    code: int


# ==============================================================================
# Get User
# ==============================================================================
class UserGet(BaseModel):
    id: int
    phone_number: str
    full_name: str
    role: UserRole

    class Config:
        from_attributes = True



# ==============================================================================
# Login with OTP
# ==============================================================================
class OTPLogin(BaseModel):
    phone_number: str



# ==============================================================================
# Pait Token
# ==============================================================================
class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
