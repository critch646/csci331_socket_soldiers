from typing import Union
import datetime as dt

from dateutil.parser import parse

class User:
    name: str
    created_at: dt.datetime
    status: bool
    
    def __init__(self, name: str, created_at: dt.datetime, status: bool = False):
        self.name = name
        self.status = status
        if isinstance(created_at, dt.datetime):
            self.created_at = created_at
        elif isinstance(created_at, str):
            self.created_at = parse(created_at)
        else:
            raise ValueError("The given created_at value did not match a recognized type. Supply either a datetime string or object")
        
    def set_status(self, status: bool):
        self.status = status
        
    @property
    def online(self):
        return self.status
    
    def __str__(self):
        return self.name
    
    __repr__ = __str__


class Message:
    content: str
    sender: User
    sent_at: dt.datetime
    
    def __init__(self, content: str, sender: User, sent_at: Union[dt.datetime, str] = dt.datetime.now()):
        self.content = content
        self.sender = sender
        if isinstance(sent_at, dt.datetime):
            self.sent_at = sent_at
        elif isinstance(sent_at, str):
            self.sent_at = parse(sent_at)
        else:
            raise ValueError("The given sent_at value did not match a recognized type. Supply either a datetime string or object")

    def date_str(self):
        """ Returns the date string for the message send date """
        return self.sent_at.strftime("%Y-%m-%d")
    
    def time_str(self):
        """Returns the time string for the message send time
        """
        return self.sent_at.strftime("%H:%M")

    def datetime_str(self) -> str:
        """Returns the datetime string for the message send datetime
        """
        return self.sent_at.strftime("%Y-%m-%d-%H:%M")

    def __str__(self):
        return f"{self.sender} ({self.time_str()}) - {self.content}"
    
    __repr__ = __str__
