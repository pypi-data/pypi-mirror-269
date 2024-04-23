import dataclasses
from typing import (
    Any,
)


@dataclasses.dataclass
class BaseSchema:
    def model_dump(self, exclude_none: bool = False) -> dict[Any, Any]:
        if exclude_none:
            return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}
        return dataclasses.asdict(self)


@dataclasses.dataclass
class SignUpSchema(BaseSchema):
    username: str
    telegram_id: int | None = None
    password: str | None = None


@dataclasses.dataclass
class LoginSchema(BaseSchema):
    username: str
    password: str


@dataclasses.dataclass
class TMELoginSchema(BaseSchema):
    telegram_id: int
    signature: str
    nonce: int
    timestamp: int


@dataclasses.dataclass
class RoleSchema(BaseSchema):
    title: str


@dataclasses.dataclass
class UserSchema(BaseSchema):
    username: str | None = None
    language: str | None = None


@dataclasses.dataclass
class ResetPasswordSchema(BaseSchema):
    old_password: str
    new_password: str
    repeat_password: str
