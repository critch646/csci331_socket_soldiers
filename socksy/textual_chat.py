import os
import datetime as dt

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Static, Button, Input, Label, ListView, ListItem

from modules.chat_data import Message, User


# set up initial state
USERNAME = os.getlogin()
CURRENT_USER = User(USERNAME, dt.datetime.now())


class MessageLabel(ListItem):
    """Single message to be formatted with the author's name and send date
    """
    def __init__(self, message: Message):
        self.message = message
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(f"{self.message.sender} ({self.message.sent_at}): {self.message.content}")


class UserList(ListView):
    def compose(self) -> ComposeResult:
        yield ListItem(Label("bob"))
        yield ListItem(Label("sally"))


class ChannelList(ListView):
    def compose(self) -> ComposeResult:
        yield ListItem(Label("general"))
        yield ListItem(Label("help"))
        yield ListItem(Label("random"))


class MessageList(ListView):
    """A scrollable list of messages to be displayed prominently on the screen
    """

    def __init__(self, messages: list[Message]):
        self.messages = messages
        super().__init__()

    def compose(self) -> ComposeResult:

        for message in self.messages:
            yield MessageLabel(message)

    def add_message(self, message: Message):
        self.append(MessageLabel(message))


class MessageEntry(Static):
    """The message input box and send button
    """

    def compose(self) -> ComposeResult:
        yield Input(id='message-box')
        yield Button('>', id='send-button')


class MessageApp(App):
    """Main class for textual window application"""

    CSS_PATH = "stylesheets/message_window.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("enter", "send_msg", "Send Message")]

    def __init__(self, messages: list[Message]):
        self.messages = messages
        super().__init__()

    def pop_msg_box_content(self):
        message_content = self.query_one('#message-box').value
        self.query_one('#message-box').value = ""  # clear the box
        return message_content

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'send-button':
            message_content = self.pop_msg_box_content()

            if message_content and not message_content.isspace():
                message = Message(message_content, CURRENT_USER)
                self.query_one('MessageList').add_message(message)

    def on_key(self, event: events.Key):
        if event.key == 'enter':
            self.query_one('#send-button').press()

    def add_message(self, message: Message):
        self.query_one('MessageList').add_message(message)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Vertical(
            Container(MessageList(self.messages), id='messages'),
            Container(UserList(), ChannelList(), id='sidebar'),
            Container(MessageEntry(), id='message-entry'),
            id='main-content'
        )
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":

    user_dict = {
        'bob': User('Bob', dt.datetime.now()),
        'alice': User('Alice', dt.datetime.now())
    }

    users = list(user_dict.values())

    messages = [
        Message("Hello world!", user_dict['alice'],    "10:33am"),
        Message("Hi Alice.",    user_dict['bob'],      "10:33am"),
        Message("How are you?", user_dict['alice'],    "10:33am"),
        Message("I'm good, thanks.", user_dict['bob'], "10:33am"),
        Message("bye", user_dict['bob'], "10:33am")
    ]

    app = MessageApp(messages)
    app.run()
