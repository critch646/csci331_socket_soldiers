"""
Flask SocketIO event handlers.

@name: server_socket_handlers.py
"""

import datetime
from flask_socketio import SocketIO

from __main__ import socketio

@socketio.on('connect')
def handle_connect():
    """
    Triggered when a client connects to the server.

    @return: None
    """

    print("socket connected")

@socketio.on('socksy_authenticate')
def handle_socksy_authenticate(username, password):
    """
    Triggered when a connected user sends their credentials for authentication

    @param username: The username of the connected client.
    @param password: The password of the connected client.
    @return: None
    """
    print(f'socksy_authenticate, username: {username}, password: {"*" * len(password)}')

@socketio.on('disconnect')
def handle_disconnect():
    """
    Triggered when a client disconnects.

    @return: None
    """

    print('Client disconnected')

@socketio.on('message')
def handle_message(username, msg, date_time):
    """
    Triggered when a client sends a message.

    @param username: Username of the sender.
    @param msg: The content of the message.
    @param date_time: The datetime the message was sent.
    @return:
    """

    t = datetime.datetime.now
    date_time_now = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')

    # TODO line below seems to now work while the 'broadcast=True' argument is present, when left out-- the server DOES receive the message sent by the client
    socketio.emit('message', data=(username, msg, date_time_now), broadcast=True)

    print(f'{username}@{date_time_now}: {msg}')


