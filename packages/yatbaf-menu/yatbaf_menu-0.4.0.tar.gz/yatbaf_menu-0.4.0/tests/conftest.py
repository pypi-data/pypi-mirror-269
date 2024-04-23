import unittest.mock as mock

import pytest

from yatbaf.router import OnCallbackQuery
from yatbaf.types import CallbackQuery
from yatbaf.types import User
from yatbaf_menu.payload import Payload


@pytest.fixture
def router():
    return OnCallbackQuery()


@pytest.fixture
def prefix():
    return "aa00aa"


@pytest.fixture
def payload(prefix):
    return Payload(prefix)


@pytest.fixture
def user():
    return User(
        id=12345,
        is_bot=False,
        first_name="Test",
    )


@pytest.fixture
def callback_query(user):
    return CallbackQuery(
        id=12345,
        chat_instance="test",
        from_=user,
    )


@pytest.fixture
def mock_mark():
    return mock.Mock()


@pytest.fixture
def handler_fn(mock_mark):

    async def fn(_):  # noqa: U101
        mock_mark()

    return fn
