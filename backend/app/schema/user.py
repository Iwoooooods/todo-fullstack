from pydantic import BaseModel


class BaseUserQueryRequest(BaseModel):
    id: int | None = None
    username: str | None = None
    email: str | None = None
    disabled: bool | None = None


class UserLoginRequest(BaseUserQueryRequest):
    username: str | None = None
    email: str | None = None
    password: str
    # username and email cannot be both empty


class DbUserQueryRequest(BaseUserQueryRequest):
    username: str
    hashed_password: str


class UserCreateRequest(BaseUserQueryRequest):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class BaseUserQueryResponse(BaseUserQueryRequest):
    id: int
    username: str
    email: str | None
    disabled: bool
