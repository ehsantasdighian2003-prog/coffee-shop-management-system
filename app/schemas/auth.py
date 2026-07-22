from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    password: str = Field(
        ...,
        min_length=8
    )

    first_name: str | None = None

    last_name: str | None = None

    email: EmailStr | None = None

    phone_number: str | None = None

    profile_image: str | None = None



class UserLogin(BaseModel):

    username: str

    password: str



class Token(BaseModel):

    access_token: str

    token_type: str



class RegisterResponse(BaseModel):

    message: str

    user_id: int