from typing import Union
import datetime as dt

from dateutil.parser import parse


class User:
    """A user object for the chat client

    Attributes:
        name (str): The name of the user
        created_at (datetime): The date and time the user was created
        status (bool): The online status of the user

    Methods:
        set_status(status): Sets the online status of the user
        online: Returns the online status of the user
    """

    name: str
    created_at: dt.datetime
    status: bool

    def __init__(self, name: str, created_at: str, status: bool = False):
        """Initializes a new user object

        Args:
            name (str): User name
            created_at (dt.datetime): The date and time the user was created
            status (bool, optional): Whether the user is online. Defaults to False.
        """
        self.name = name
        self.status = status
        self.created_at = created_at

    def set_status(self, status: bool):
        self.status = status

    @property
    def online(self):
        return self.status

    def __str__(self):
        return self.name

    __repr__ = __str__


class Message:
    """A message object for the chat client

    Attributes:
        content (str): The content of the message
        sender (User): The user who sent the message
        sent_at (str): The date and time the message was sent

    Methods:
        date_str(): Returns the date string for the message send date
        time_str(): Returns the time string for the message send time
        datetime_str(): Returns the datetime string for the message send datetime
    """

    content: str
    sender: User
    sent_at: str

    def __init__(self, content: str, sender: User, sent_at: str = None):
        """Initializes a new message object

        Args:
            content (str): What the message contains e.g. "Hello there Bob!"
            sender (User): The user who sent the message
            sent_at (str, optional): When the message was sent. Defaults to None.
        """
        self.content = content
        self.sender = sender
        self.sent_at = sent_at

    def date_str(self):
        """ Returns the date string for the message send date """
        return self.sent_at

    def time_str(self):
        """Returns the time string for the message send time
        """
        return self.sent_at

    def datetime_str(self) -> str:
        """Returns the datetime string for the message send datetime
        """
        return self.sent_at

    def __str__(self):
        return f"{self.sender} ({self.time_str()}) - {self.content}"

    __repr__ = __str__
