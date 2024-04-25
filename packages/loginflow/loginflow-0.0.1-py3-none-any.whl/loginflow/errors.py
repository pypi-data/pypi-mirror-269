from enum import StrEnum


class Message(StrEnum):
    InputRequired = "This field is required"
    UnknownUsername = "Username not found"
    UnknownEmail = "Email not found"
    InvalidPassword = "Invalid password"
    ContainsNullByte = "Field cannot contain null bytes"
    InvalidEmail = "Not a valid email address"


class LoginFlowException(Exception):
    pass


class AccountDoesNotExist(LoginFlowException):
    pass


class InvalidAccount(LoginFlowException):
    pass


class InputError(LoginFlowException):
    errors: dict[str, Message]

    def __init__(self, errors: dict[str, Message]):
        self.errors = errors


class InvalidToken(LoginFlowException):
    pass


class TokenExpired(InvalidToken):
    pass


class EmailAlreadyVerified(LoginFlowException):
    pass
