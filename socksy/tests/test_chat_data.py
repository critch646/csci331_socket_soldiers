"""
Unit tests for chat_data module. Tests the User and Message classes.

These are very simple in nature, only testing basic functionality.
They ensure the classes hold the correct data/methods and that values
can be grabbed and manipulated as expected.

@name: test_chat_data
@author: Ethan Posner
@Date: 2023/04/08
"""

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
