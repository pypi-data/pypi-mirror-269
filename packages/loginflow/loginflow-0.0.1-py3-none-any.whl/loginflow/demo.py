from dataclasses import dataclass
from typing import Callable, TypeAlias

import bcrypt

from ._core import Event
from .errors import InputError, InvalidAccount, Message


@dataclass(frozen=True, kw_only=True)
class Account:
    username: str
    auth_info: str


@dataclass(frozen=True, kw_only=True)
class NewAccount(Event):
    username: str
    auth_info: str


@dataclass(frozen=True, kw_only=True)
class QueryByName(Event):
    username: str


@dataclass(frozen=True, kw_only=True)
class Login(Event):
    username: str


CheckPassword: TypeAlias = Callable[[Account | None], Login]


class LoginFlow:
    _bcrypt_rounds: int = 12

    def _validate_input(
        self, *, username: str | None, password: str | None
    ) -> tuple[str, str]:
        errors: dict[str, Message] = {}

        username = username or ""
        password = password or ""

        if not username.strip():
            errors["username"] = Message.InputRequired
        if not password:
            errors["password"] = Message.InputRequired

        if "\0" in username:
            errors["username"] = Message.ContainsNullByte
        if "\0" in password:
            errors["password"] = Message.ContainsNullByte

        if errors:
            raise InputError(errors)

        return (username, password)

    def register(self, *, username: str | None, password: str | None) -> NewAccount:
        username, password = self._validate_input(username=username, password=password)
        pw_hash = bcrypt.hashpw(
            password.encode("utf-8"), salt=bcrypt.gensalt(rounds=self._bcrypt_rounds)
        )

        return NewAccount(username=username, auth_info=pw_hash.decode("ascii"))

    def login(
        self, *, username: str | None, password: str | None
    ) -> tuple[QueryByName, CheckPassword]:
        username, password = self._validate_input(username=username, password=password)

        def _check_password(account: Account | None, /) -> Login:
            if account is None:
                raise InputError({"username": Message.UnknownUsername})
            if account.username != username:
                raise InvalidAccount
            return self._check_password(account, password=password)

        return QueryByName(username=username), _check_password

    def _check_password(self, account: Account, /, password: str) -> Login:
        if bcrypt.checkpw(password.encode("utf-8"), account.auth_info.encode("ascii")):
            return Login(username=account.username)
        raise InputError({"password": Message.InvalidPassword})
