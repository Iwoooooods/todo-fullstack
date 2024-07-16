from enum import Enum


class LoginError(Enum):
    USER_NOT_FOUND = 1
    INCORRECT_PASSWORD = 2
