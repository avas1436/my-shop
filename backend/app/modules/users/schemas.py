from pydantic import BaseModel, EmailStr

from app.common.enums import UserRole


# ==============================================================================
# Register User and Login
# ==============================================================================
class RegisterUser(BaseModel):
    name: str
    phone_number: int

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
