from unittest.mock import ANY

import pytest
from pytest import raises as assert_raises

from loginflow.demo import Account, Login, LoginFlow, NewAccount, QueryByName
from loginflow.errors import InputError, InvalidAccount, Message


@pytest.fixture
def flow() -> LoginFlow:
    flow = LoginFlow()
    # use reduced number of bcrypt rounds for faster tests (insecure!)
    flow._bcrypt_rounds = 4  # pyright: ignore[reportPrivateUsage]
    return flow


@pytest.fixture
def account(flow: LoginFlow) -> Account:
    new_account = flow.register(username="fred", password="tomato")
    return Account(username=new_account.username, auth_info=new_account.auth_info)


def test_can_register(flow: LoginFlow):
    new_account = flow.register(username="fred", password="tomato")

    assert new_account == NewAccount(username="fred", auth_info=ANY)
    assert new_account.auth_info.startswith("$2b$")


@pytest.mark.parametrize("username", ["", None])
def test_register_with_empty_username_raises_inputerror(
    flow: LoginFlow, username: str | None
):
    with assert_raises(InputError) as exc_info:
        _ = flow.register(username=username, password="tomato")

    assert exc_info.value.errors == {"username": Message.InputRequired}


@pytest.mark.parametrize("password", ["", None])
def test_register_with_empty_password_raises_inputerror(
    flow: LoginFlow, password: str | None
):
    with assert_raises(InputError) as exc_info:
        _ = flow.register(username="fred", password=password)

    assert exc_info.value.errors == {"password": Message.InputRequired}


def test_register_username_with_null_byte_raises_inputerror(flow: LoginFlow):
    with assert_raises(InputError) as exc_info:
        _ = flow.register(username="fred\0", password="tomato")

    assert exc_info.value.errors == {"username": Message.ContainsNullByte}


def test_register_password_with_null_byte_raises_inputerror(flow: LoginFlow):
    with assert_raises(InputError) as exc_info:
        _ = flow.register(username="fred", password="tomato\0")

    assert exc_info.value.errors == {"password": Message.ContainsNullByte}


def test_cannot_login_with_unknown_username(flow: LoginFlow):
    _, check_password = flow.login(username="fred", password="tomato")

    with assert_raises(InputError) as exc_info:
        _ = check_password(None)

    assert exc_info.value.errors == {"username": Message.UnknownUsername}


def test_cannot_login_with_invalid_password(flow: LoginFlow, account: Account):
    _, check_password = flow.login(username="fred", password="potato")

    with assert_raises(InputError) as exc_info:
        _ = check_password(account)

    assert exc_info.value.errors == {"password": Message.InvalidPassword}


def test_can_login_with_correct_username_and_password(
    flow: LoginFlow, account: Account
):
    query, check_password = flow.login(username="fred", password="tomato")

    assert query == QueryByName(username="fred")
    assert check_password(account) == Login(username="fred")


def test_check_password_account_must_match_name(flow: LoginFlow, account: Account):
    query, check_password = flow.login(username="fred", password="tomato")

    assert query == QueryByName(username="fred")

    with assert_raises(InvalidAccount):
        _ = check_password(Account(username="barney", auth_info=account.auth_info))


@pytest.mark.parametrize("username", ["", None])
def test_login_with_empty_username_raises_inputerror(
    flow: LoginFlow, username: str | None
):
    with assert_raises(InputError) as exc_info:
        _ = flow.login(username=username, password="tomato")

    assert exc_info.value.errors == {"username": Message.InputRequired}


@pytest.mark.parametrize("password", ["", None])
def test_login_with_empty_password_raises_inputerror(
    flow: LoginFlow, password: str | None
):
    with assert_raises(InputError) as exc_info:
        _ = flow.login(username="fred", password=password)

    assert exc_info.value.errors == {"password": Message.InputRequired}


def test_login_username_with_null_byte_raises_inputerror(flow: LoginFlow):
    with assert_raises(InputError) as exc_info:
        _ = flow.login(username="fred\0", password="tomato")

    assert exc_info.value.errors == {"username": Message.ContainsNullByte}


def test_login_password_with_null_byte_raises_inputerror(flow: LoginFlow):
    with assert_raises(InputError) as exc_info:
        _ = flow.login(username="fred", password="tomato\0")

    assert exc_info.value.errors == {"password": Message.ContainsNullByte}
