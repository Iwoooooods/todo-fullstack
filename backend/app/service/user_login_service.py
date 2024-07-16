import jwt
import bcrypt

from loguru import logger
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from app.model.user import User
from app.repository.user_login_repository import LoginRepository, get_repository
from app.schema.user import TokenData, UserLoginRequest, \
    UserCreateRequest, BaseUserQueryResponse
from app.const import LoginError


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LoginService:
    def __init__(self, repo: LoginRepository):
        self.repo = repo

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_password_hash(password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode('utf-8')

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> Response:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return JSONResponse(content={"msg": "User Not Found!"}, status_code=status.HTTP_404_NOT_FOUND)
            token_data = TokenData(username=username)
        except (InvalidTokenError, ExpiredSignatureError) as error:
            logger.error(error)
            if isinstance(error, ExpiredSignatureError):
                return JSONResponse(content={"msg": "Token expired"}, status_code=status.HTTP_401_UNAUTHORIZED)
            return JSONResponse(content={"msg": "Invalid token"}, status_code=status.HTTP_401_UNAUTHORIZED)
        user: User = await self.repo.get_user_by_email_or_name(username=token_data.username, email=None)
        if user is None:
            return JSONResponse(content={"msg": "User not found"}, status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content={"me": BaseUserQueryResponse(**user.to_dict()).model_dump()},
                            status_code=status.HTTP_200_OK)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        password_byte_enc = plain_password.encode('utf-8')
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)

    async def authenticate_user(self, req: UserLoginRequest) -> User | LoginError:
        user = await self.repo.get_user_by_email_or_name(email=req.email, username=req.username)
        if not user:
            return LoginError.USER_NOT_FOUND
        if not self.verify_password(req.password, bytes(user.hashed_password, "utf-8")):
            return LoginError.INCORRECT_PASSWORD
        return user

    async def create_user(self, req: UserCreateRequest) -> Response:
        hashed_password = self.get_password_hash(req.password)
        user: User = User(username=req.username, hashed_password=hashed_password, email=req.email)
        try:
            user = await self.repo.add_user(user)
        except Exception as ex:
            logger.error(ex)
            return JSONResponse({"msg": "Internal Server Error!"}, status_code=500)
        return JSONResponse(**user.to_dict(), status_code=status.HTTP_201_CREATED)


async def get_login_service(repo: LoginRepository = Depends(get_repository)) -> LoginService:
    return LoginService(repo)
