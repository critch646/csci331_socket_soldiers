"""
The main entry for the Socksy server.

@name: socksy_server
"""

# Standard library imports
import datetime
import threading
import time
import socket
import random


# Third-party imports
from flask import Flask, request, redirect, render_template
from flask_socketio import SocketIO


# Project imports
from modules.server_socketio import socketio_server, socksyServer
from modules.server_socket_handlers import handle_connect, handle_socksy_authenticate, handle_disconnect, handle_message
from modules.servermariadb import DatabaseConnection

DEBUG = True
TEST = False


def flask_thread(debug: bool, host: str, port: int):
    """
    Thread function to run the flask socketio server.

    @param debug: True if you want to run the server in debug mode.
    @param host: The host address to run the server with.
    @param port: The port number to run the server with.
    @return: None
    """
    socketio_server.run(socksyServer, debug=debug, host=host, port=port)


def test_emit_message_thread():
    """
    For testing. See if connected clients receive messages.

    @return: None
    """

    print('test_emit_message thread started.')

    while TEST:
        time.sleep(10 + random.randint(0, 5))
        date_time_now = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        msg = f'Here\'s a new int! {random.randint(1, 1024)}'
        socketio_server.emit('message', ('server', msg, date_time_now), broadcast=True)
        print(f'message sent@{date_time_now}: {msg}')


if __name__ == '__main__':
    print(f'Starting Socksy Server...')

    ipAddress = ""

    # Get hostname and ip address
    try:
        hostname = socket.gethostname()
        ipAddress = socket.gethostbyname(hostname)
    except socket.error as e:
        print(e)
        ipAddress = '127.0.0.1'

    hostPort = 6000
    print(f'Server IP address: \'{ipAddress}:{hostPort}\'')

    # Run test message emits to connected clients.
    if DEBUG and TEST:
        testEmitMessageThread = threading.Thread(target=test_emit_message_thread)
        testEmitMessageThread.start()

    # # Start database connection for use for server
    # dolphin_db = DatabaseConnection()

    # Run Flask app with SocketIO wrapper. Set host with static IP
    flaskApp = threading.Thread(target=flask_thread(DEBUG, ipAddress, hostPort))
    flaskApp.start()
