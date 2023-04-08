"""
The main entry point for the Socksy server.

@name: socksy_server.py
@author: Zeke Critchlow
@date: 2023/04/08
"""

# Standard library imports
import threading
import socket

# Third-party imports
from flask import Flask, request, redirect, render_template
from flask_socketio import SocketIO

# Project imports
from modules.server_db_connect import dolphin_db
from modules.server_socketio import socketio_server, socksyServer
from modules.server_socket_handlers import handle_connect, handle_socksy_authenticate, handle_disconnect, handle_message

DEBUG = True


def flask_thread(debug: bool, host: str, port: int):
    """
    Thread function to run the flask socketio server.

    @param debug: True if you want to run the server in debug mode.
    @param host: The host address to run the server with.
    @param port: The port number to run the server with.
    @return: None
    """
    socketio_server.run(socksyServer, debug=debug, host=host, port=port)


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
    print(f'Server address: \'{ipAddress}:{hostPort}\'')

    # Run Flask app with SocketIO wrapper. Set host with static IP
    flaskApp = threading.Thread(target=flask_thread(DEBUG, ipAddress, hostPort))
    flaskApp.start()
