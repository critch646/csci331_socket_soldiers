# Third-party imports
import pytest

# Local Imports
from socksy.modules.chat_data import User, Message


class TestUser:
    def test_init(self):
        test_user = User("test_user", "2021-01-01 00:00:00", status=True)
        assert test_user.created_at == "2021-01-01 00:00:00"

    def test_simple(self):
        test_user = User("test_user", "2021-01-01 00:00:00", status=True)
        assert test_user.online is True

        test_user.set_status(False)

        assert test_user.online is False


class TestMessage:
    def test_init(self):
        test_user = User("test_user", "2021-01-01 00:00:00", status=True)
        test_msg = Message("test_msg", test_user, "2021-01-01 00:00:00")

        assert test_msg.content == "test_msg"

    def test_message(self):
        test_user = User("test_user", "2021-01-01 00:00:00", status=True)
        test_msg = Message("test_msg", test_user, "2021-01-01 00:00:00")
        assert test_msg.date_str() == "2021-01-01"
        assert test_msg.time_str() == "00:00:00"
        assert test_msg.datetime_str() == "2021-01-01 00:00:00"
