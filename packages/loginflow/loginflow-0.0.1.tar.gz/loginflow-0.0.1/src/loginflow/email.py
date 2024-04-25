from dataclasses import dataclass
from typing import Callable, TypeAlias

import bcrypt
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from ._core import Event
from .errors import (
    AccountDoesNotExist,
    EmailAlreadyVerified,
    InputError,
    InvalidAccount,
    InvalidToken,
    Message,
    TokenExpired,
)


@dataclass(frozen=True, kw_only=True)
class Account:
    id: int | str
    email: str
    email_verified: bool = False
    auth_info: str


@dataclass(frozen=True, kw_only=True)
class NewAccount(Event):
    email: str
    auth_info: str


@dataclass(frozen=True, kw_only=True)
class VerificationEmail(Event):
    email: str
    token: str


@dataclass(frozen=True, kw_only=True)
class QueryById(Event):
    id: int | str


@dataclass(frozen=True, kw_only=True)
class QueryByEmail(Event):
    email: str


@dataclass(frozen=True, kw_only=True)
class UpdatedAccount(Event):
    id: int | str
    email_verified: bool
    auth_info: str


@dataclass(frozen=True, kw_only=True)
class Login(Event):
    id: int | str


GetEmailToken: TypeAlias = Callable[[Account], VerificationEmail]

ValidateEmailToken: TypeAlias = Callable[[Account | None], UpdatedAccount]

CheckPassword: TypeAlias = Callable[[Account | None], Login]


class LoginFlow:
    _bcrypt_rounds: int = 12

    def __init__(self, /, secret: str | bytes, email_token_max_age: int = 60 * 60 * 30):
        self._email_token_max_age = email_token_max_age
        self._email_token_signer = URLSafeTimedSerializer(
            secret_key=secret, salt="loginflow.email_token"
        )

    def _validate_email_and_password(
        self, *, email: str | None, password: str | None
    ) -> tuple[str, str]:
        errors: dict[str, Message] = {}

        email = email or ""
        password = password or ""

        if not email:
            errors["email"] = Message.InputRequired
        if not password:
            errors["password"] = Message.InputRequired

        if "\0" in email:
            errors["email"] = Message.ContainsNullByte
        if "\0" in password:
            errors["password"] = Message.ContainsNullByte

        if errors:
            raise InputError(errors)

        return (email, password)

    def _validate_new_email_and_password(
        self, *, email: str | None, password: str | None
    ) -> tuple[str, str]:
        errors: dict[str, Message] = {}

        email, password = self._validate_email_and_password(
            email=email, password=password
        )

        # Check that the email has the form <local_part>@<domain_part>, and
        # the domain has at least two parts (name + tld).
        # This will accept invalid email addresses, and will reject some
        # technically valid ones like username@localhost (but we don't care
        # about those).
        local_part, _, domain_part = email.partition("@")
        name, _, tld = domain_part.rpartition(".")
        if not (local_part and domain_part and name and tld):
            errors["email"] = Message.InvalidEmail

        if errors:
            raise InputError(errors)

        return (email, password)

    def register(
        self, *, email: str | None, password: str | None
    ) -> tuple[NewAccount, GetEmailToken]:
        email, password = self._validate_new_email_and_password(
            email=email, password=password
        )

        pw_hash = bcrypt.hashpw(
            password.encode("utf-8"), salt=bcrypt.gensalt(rounds=self._bcrypt_rounds)
        )

        return (
            NewAccount(email=email, auth_info=pw_hash.decode("ascii")),
            self._get_email_token,
        )

    def _get_email_token(self, account: Account) -> VerificationEmail:
        token = self._email_token_signer.dumps(account.id)
        return VerificationEmail(email=account.email, token=token)

    def verify_email(self, *, token: str) -> tuple[QueryById, ValidateEmailToken]:
        try:
            account_id = self._email_token_signer.loads(
                token, max_age=self._email_token_max_age
            )
        except SignatureExpired:
            raise TokenExpired
        except BadSignature:
            raise InvalidToken

        def _validate_email_token(account: Account | None) -> UpdatedAccount:
            if account is None:
                raise AccountDoesNotExist
            if account.id != account_id:
                raise InvalidAccount
            return self._validate_email_token(account)

        return (QueryById(id=account_id), _validate_email_token)

    def _validate_email_token(self, account: Account) -> UpdatedAccount:
        return UpdatedAccount(
            id=account.id, email_verified=True, auth_info=account.auth_info
        )

    def resend_verification_email(self, account: Account) -> VerificationEmail:
        if account.email_verified:
            raise EmailAlreadyVerified
        return self._get_email_token(account)

    def login(
        self, *, email: str | None, password: str | None
    ) -> tuple[QueryByEmail, CheckPassword]:
        email, password = self._validate_email_and_password(
            email=email, password=password
        )

        def _check_password(account: Account | None, /) -> Login:
            if not account:
                raise InputError({"email": Message.UnknownEmail})
            if account.email != email:
                raise InvalidAccount
            return self._check_password(account, password=password)

        return QueryByEmail(email=email), _check_password

    def _check_password(self, account: Account, /, password: str) -> Login:
        if bcrypt.checkpw(password.encode("utf-8"), account.auth_info.encode("ascii")):
            return Login(id=account.id)
        raise InputError({"password": Message.InvalidPassword})
