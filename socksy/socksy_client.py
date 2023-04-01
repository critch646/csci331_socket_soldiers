"""


:name: socksy_client
"""

# Standard library imports
import logging.config
import os
from pathlib import Path
import queue
import sys
import threading
import time
import socket
import asyncio
import getpass
import datetime as dt

# Third-party Imports
import socketio
import pyjson5

# Local Imports
from modules.chat_data import Message, User
import window

socketio = socketio.Client()

# when a message is received through the socket connection, it is added to this queue
# the main thread will check this queue and update the GUI
MESSAGE_QUEUE = queue.Queue()

USERNAME = getpass.getuser()  # Even Python suggest not using getlogin()
CURRENT_USER = User(USERNAME, dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@socketio.on('my_message')
def on_message(data):
    print('I received a message: ', data)


@socketio.event
def connect():
    print('I am connected!')


@socketio.event
def connect_error(data):
    print('Connection Error: ', data)


def socksy_emit_authenticate(username, password):
    socketio.emit('socksy_authenticate', data=(username, password))


@socketio.event
def disconnect():
    print('Disconnected')


@socketio.on('message')
def handle_socket_message(username, msg, date_time):
    print(f'{username} ({date_time}): {msg}')
    # XXX: Messags are added to the queue here
    message = Message(msg, username, date_time)
    MESSAGE_QUEUE.put(message, timeout=3)


@socketio.on('update_message_history')
def handle_socket_update_message_history(messages):
    print('handle_socket_update_message_history')
    for msg in messages:
        print(msg)

def send_socket_message(username, msg, date_time):
    print(f'send_socket_message, username: {username}, msg: {msg}, datetime: {date_time}')
    socketio.emit('message', data=(username, msg, date_time))
    # XXX: This is called when the user presses enter in the input box or clicks the send button


def socketio_connect_thread(connectionStr: str):

    print('Attempting to connect socketio')
    socketio.connect(connectionStr)


if __name__ == '__main__':

    socketio_connection = threading.Thread(target=socketio_connect_thread, args=['http://192.168.18.43:6000'])
    socketio_connection.start()

    style_data = {}

    style_file = Path().cwd() / 'socksy' / 'tk_interface_style.json'
    if style_file.exists():
        print(f"File {style_file.name} exists. Using its style.")
        with open(style_file, 'r') as fp:
            style_data = pyjson5.decode_io(fp)
    root = window.Root(style_data, message_send_command=send_socket_message)
    root.lift()  # Tells OS to bring window to front

    root.update()  # This is required to make the GUI appear
    root.mainloop()  # This is the main loop that runs the GUI
