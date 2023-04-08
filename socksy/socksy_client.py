"""
Runs the chat window and connects to the main socket server (if it is running).
Gets the hostname of the socket server from `socksy/client.env`.

@name: socksy_server
@author: Ethan Posner and Zeke Critchlow
@Date: 2023/04/08
"""

# Standard library imports
import os
from pathlib import Path
import queue
import threading
import getpass
import datetime as dt

# Third-party Imports
import socketio
import pyjson5
from dotenv import load_dotenv

# Local Imports
from modules.chat_data import Message, User
import window

if Path('socksy/client.env').exists():
    load_dotenv('socksy/client.env')
elif Path('client.env').exists():
    load_dotenv('client.env')
else:
    raise FileNotFoundError('client.env not found')

assert os.environ.get('SERVER_HOSTNAME', None) is not None, 'SERVER_HOSTNAME must be set in socksy/.env.user'

socketio = socketio.Client()

# when a message is received through the socket connection, it is added to this queue
# the main thread will check this queue and update the GUI
MESSAGE_QUEUE = queue.Queue()

MESSAGE_HISTORY_FETCHED = False # Used to prevent client from updating message history multiple times.

USERNAME = getpass.getuser()  # Even Python suggest not using getlogin()
CURRENT_USER = User(USERNAME, dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@socketio.event
def connect() -> None:
    """
    Event triggered when client connects to socket server.

    @return: None
    """

    print('Client connected to server!')
    print(f'    SID: {socketio.sid}')
    print(f'    Transport: {socketio.transport()}')


@socketio.event
def connect_error(data) -> None:
    """
    Event triggered when there is an error when connecting to the server.

    @param data: data associated with the error event.
    @return: None
    """
    print('Connection Error: ', data)


def socksy_emit_authenticate(username: str, password: str) -> None:
    """
    Used to authenticate the client with the server.
    #TODO: stretch goal

    @param username: The username of the client
    @param password: The client's password
    @return: None
    """
    socketio.emit('socksy_authenticate', data=(username, password))


@socketio.event
def disconnect() -> None:
    """
    Even triggered when the client disconnects from the server.

    @return: None
    """
    print('Disconnected')


@socketio.on('message')
def handle_socket_message(username, msg, date_time) -> None:
    """
    Event triggered when the client receives a 'message' event from the
    socket server. Adds received message to the client message queue.

    @param username: The username of the client.
    @param msg: The message content.
    @param date_time: The date and time the message was sent.
    @return:
    """

    global MESSAGE_QUEUE
    print(f'{username} ({date_time}): {msg}')
    message = Message(msg, username, date_time)
    MESSAGE_QUEUE.put(message, timeout=3)


@socketio.on('update_message_history')
def handle_socket_update_message_history(serial_messages) -> None:
    """
    Event triggered when the client receives a 'update_message_history' event
    from the socket server. Adds the list of messages to the message queue.

    @param serial_messages: A list of dictionary objects representing
     message objects
    @return: None
    """

    global MESSAGE_HISTORY_FETCHED
    if not MESSAGE_HISTORY_FETCHED:
        MESSAGE_HISTORY_FETCHED = True
        global MESSAGE_QUEUE
        messages = []
        for serial_msg in serial_messages:
            msg = Message(serial_msg['content'], User(serial_msg['user'], '', True), serial_msg['sent_at'])
            MESSAGE_QUEUE.put(msg)


def send_socket_message(username, msg, date_time) -> None:
    """
    Sends a message to the server.

    NOTE: This is called when the user presses `ENTER` in the input box or
        clicks the send button

    @param username: The username of the client.
    @param msg: The content of the message.
    @param date_time: The date and time the message was sent.
    @return: None
    """

    socketio.emit('message', data=(username, msg, date_time))


def socketio_connect_thread(connection: str, namespace: str) -> None:
    """
    Thread function starts the socketIO client and connects to the socket server.

    @param connection: The server address to connect to.
    @param namespace: The namespace to connect to.
    @return: None
    """
    print('Attempting to connect socketio')
    socketio.connect(connection, namespaces=namespace)


if __name__ == '__main__':

    # Get the hostname
    hostname = os.environ.get('SERVER_HOSTNAME', '127.0.0.1')

    # Setup socket_connection thread
    socketio_connection = threading.Thread(target=socketio_connect_thread, args=[f'http://{hostname}:6000', '/'])
    socketio_connection.start()

    # Setup TKinter style
    style_data = {}
    style_file = Path().cwd() / 'socksy' / 'tk_interface_style.json'
    if style_file.exists():
        print(f"File {style_file.name} exists. Using its style.")
        with open(style_file, 'r') as fp:
            style_data = pyjson5.decode_io(fp)

    # Setup root Tkinter window
    root = window.Root(style_data, message_send_command=send_socket_message, message_queue=MESSAGE_QUEUE, current_user=CURRENT_USER)
    root.lift()  # Tells OS to bring window to front

    root.update()  # This is required to make the GUI appear
    root.mainloop()  # This is the main loop that runs the GUI
