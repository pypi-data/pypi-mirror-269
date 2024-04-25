from unittest.mock import ANY

import pytest
from itsdangerous import URLSafeTimedSerializer
from pytest import raises as assert_raises

from loginflow.email import (
    Account,
    Login,
    LoginFlow,
    NewAccount,
    QueryByEmail,
    QueryById,
    UpdatedAccount,
    VerificationEmail,
)
from loginflow.errors import (
    AccountDoesNotExist,
    EmailAlreadyVerified,
    InputError,
    InvalidAccount,
    InvalidToken,
    Message,
    TokenExpired,
)


@pytest.fixture
def flow() -> LoginFlow:
    flow = LoginFlow(secret="The dancing porcupine.")
    # use reduced number of bcrypt rounds for faster tests (insecure!)
    flow._bcrypt_rounds = 4  # pyright: ignore[reportPrivateUsage]
    return flow


@pytest.fixture
def account_and_email_token(flow: LoginFlow) -> tuple[Account, str]:
    new_account, get_email_token = flow.register(
        email="fred@example.net", password="tomato"
    )
    account = Account(id=1, email=new_account.email, auth_info=new_account.auth_info)
    email_token = get_email_token(account)
    return account, email_token.token


@pytest.fixture
def account(account_and_email_token: tuple[Account, str]) -> Account:
    return account_and_email_token[0]


def test_can_register(flow: LoginFlow):
    new_account, get_email_token = flow.register(
        email="fred@example.net", password="tomato"
    )

    assert new_account == NewAccount(email="fred@example.net", auth_info=ANY)
    assert new_account.auth_info.startswith("$2b$")

    account = Account(id=1, email=new_account.email, auth_info=new_account.auth_info)
    verification_email = get_email_token(account)

    assert verification_email == VerificationEmail(email="fred@example.net", token=ANY)


@pytest.mark.parametrize("email", ["", None])
def test_register_with_empty_email_raises_inputerror(
    flow: LoginFlow, email: str | None
):
    with assert_raises(InputError) as exc_info:
        _ = flow.register(email=email, password="tomato")

    assert exc_info.value.errors == {"email": Message.InputRequired}


@pytest.mark.parametrize("email", ["foo", "@", "foo@", "@foo", "foo@bar"])
def test_register_with_invalid_email_raises_inputerror(
    flow: LoginFlow, email: str | None
):
    with assert_raises(InputError) as exc_info:
        _ = flow.register(email=email, password="tomato")

    assert exc_info.value.errors == {"email": Message.InvalidEmail}


@pytest.mark.parametrize("password", ["", None])
def test_register_with_empty_password_raises_inputerror(
    flow: LoginFlow, password: str | None
):
    with assert_raises(InputError) as exc_info:
        _ = flow.register(email="fred@example.net", password=password)

    assert exc_info.value.errors == {"password": Message.InputRequired}


def test_register_email_with_null_byte_raises_inputerror(flow: LoginFlow):
    with assert_raises(InputError) as exc_info:
        _ = flow.register(email="fred@example.net\0", password="tomato")

    assert exc_info.value.errors == {"email": Message.ContainsNullByte}


def test_register_password_with_null_byte_raises_inputerror(flow: LoginFlow):
    with assert_raises(InputError) as exc_info:
        _ = flow.register(email="fred@example.net", password="tomato\0")

    assert exc_info.value.errors == {"password": Message.ContainsNullByte}


def test_can_verify_email_address(
    flow: LoginFlow, account_and_email_token: tuple[Account, str]
):
    account, token = account_and_email_token
    query, validate_email_token = flow.verify_email(token=token)

    assert query == QueryById(id=1)

    updated_account = validate_email_token(account)

    assert updated_account == UpdatedAccount(id=1, email_verified=True, auth_info=ANY)


def test_validate_email_token_account_must_match_email(
    flow: LoginFlow, account_and_email_token: tuple[Account, str]
):
    account, token = account_and_email_token
    query, validate_email_token = flow.verify_email(token=token)

    assert query == QueryById(id=1)

    with assert_raises(InvalidAccount):
        _ = validate_email_token(
            Account(id=2, email=account.email, auth_info=account.auth_info)
        )


def test_email_verification_fails_with_invalid_token(
    flow: LoginFlow,
):
    with assert_raises(InvalidToken):
        _ = flow.verify_email(token="some other token")


def test_email_verification_fails_with_unknown_account(
    flow: LoginFlow, account_and_email_token: tuple[Account, str]
):
    _, token = account_and_email_token
    _, validate_email_token = flow.verify_email(token=token)

    with assert_raises(AccountDoesNotExist):
        _ = validate_email_token(None)


def test_email_verification_fails_with_expired_token():
    flow = LoginFlow(secret="The dancing porcupine.", email_token_max_age=-1)
    signer = URLSafeTimedSerializer(
        secret_key="The dancing porcupine.", salt="loginflow.email_token"
    )
    token = signer.dumps(1)

    with assert_raises(TokenExpired):
        _ = flow.verify_email(token=token)


def test_can_resend_verification_email(
    flow: LoginFlow, account_and_email_token: tuple[Account, str]
):
    account, _ = account_and_email_token
    verification_email = flow.resend_verification_email(account)

    assert verification_email == VerificationEmail(email="fred@example.net", token=ANY)


def test_resend_verification_email_fails_when_email_is_already_verified(
    flow: LoginFlow,
):
    account = Account(id=1, email="fred@example.net", email_verified=True, auth_info="")

    with assert_raises(EmailAlreadyVerified):
        _ = flow.resend_verification_email(account)


def test_cannot_login_with_unknown_email(flow: LoginFlow):
    _, check_password = flow.login(email="barney@example.net", password="tomato")

    with assert_raises(InputError) as exc_info:
        _ = check_password(None)

    assert exc_info.value.errors == {"email": Message.UnknownEmail}


def test_cannot_login_with_invalid_password(flow: LoginFlow, account: Account):
    _, check_password = flow.login(email="fred@example.net", password="potato")

    with assert_raises(InputError) as exc_info:
        _ = check_password(account)

    assert exc_info.value.errors == {"password": Message.InvalidPassword}


def test_can_login_with_correct_email_and_password(flow: LoginFlow, account: Account):
    query, check_password = flow.login(email="fred@example.net", password="tomato")

    assert query == QueryByEmail(email="fred@example.net")
    assert check_password(account) == Login(id=account.id)


def test_check_password_account_must_match_email(flow: LoginFlow, account: Account):
    query, check_password = flow.login(email="fred@example.net", password="tomato")

    assert query == QueryByEmail(email="fred@example.net")

    with assert_raises(InvalidAccount):
        _ = check_password(
            Account(id=1, email="barney@example.net", auth_info=account.auth_info)
        )


@pytest.mark.parametrize("email", ["", None])
def test_login_with_empty_email_raises_inputerror(flow: LoginFlow, email: str | None):
    with assert_raises(InputError) as exc_info:
        _ = flow.login(email=email, password="tomato")

    assert exc_info.value.errors == {"email": Message.InputRequired}


@pytest.mark.parametrize("password", ["", None])
def test_login_with_empty_password_raises_inputerror(
    flow: LoginFlow, password: str | None
):
    with assert_raises(InputError) as exc_info:
        _ = flow.login(email="fred@example.net", password=password)

    assert exc_info.value.errors == {"password": Message.InputRequired}


def test_login_email_with_null_byte_raises_inputerror(flow: LoginFlow):
    with assert_raises(InputError) as exc_info:
        _ = flow.login(email="fred@example.net\0", password="tomato")

    assert exc_info.value.errors == {"email": Message.ContainsNullByte}


def test_login_password_with_null_byte_raises_inputerror(flow: LoginFlow):
    with assert_raises(InputError) as exc_info:
        _ = flow.login(email="fred@example.net", password="tomato\0")

    assert exc_info.value.errors == {"password": Message.ContainsNullByte}
