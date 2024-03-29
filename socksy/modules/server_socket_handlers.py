"""
Flask SocketIO event handlers.

Uses Flash socketIO server instance created in `server_socketio.py`

@name: server_socket_handlers.py
@authors: Zeke Critchlow
@date: 2023/04/08
"""

import datetime
from flask_socketio import SocketIO, Namespace

from __main__ import socketio_server
from __main__ import dolphin_db
from .server_socketio import socketio_server

@socketio_server.on('connect')
def handle_connect():
    """
    Triggered when a client connects to the server.

    @return: None
    """
    print("socket connected")
    message_history_list = dolphin_db.pull_message_history()
    serializable_list = []
    for msg in message_history_list:
        msg_dict = {}
        msg_dict['content'] = msg.content
        msg_dict['user'] = msg.sender.name
        msg_dict['sent_at'] = msg.sent_at
        serializable_list.append(msg_dict)
    socketio_server.emit('update_message_history', data=serializable_list)

@socketio_server.on('socksy_authenticate')
def handle_socksy_authenticate(username: str, password: str):
    """
    Triggered when a connected user sends their credentials for authentication

    @param username: The username of the connected client.
    @param password: The password of the connected client.

    @return: None
    """
    print(f'socksy_authenticate, username: {username}, password: {"*" * len(password)}')


@socketio_server.on('disconnect')
def handle_disconnect():
    """
    Triggered when a client disconnects.

    @return: None
    """

    print('Client disconnected')


@socketio_server.on('message')
def handle_message(username: str, msg: str, date_time: str):
    """
    Triggered when a client sends a message.

    @param username: Username of the sender.
    @param msg: The content of the message.
    @param date_time: The datetime the message was sent.
    @return:
    """

    date_time_now = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')

    socketio_server.emit('message', data=(username, msg, date_time_now))

    if dolphin_db.check_user_exists(username) is False:
        dolphin_db.add_user(username)

    dolphin_db.add_message(username, msg)
    print(f'{username}@{date_time_now}: {msg}')


