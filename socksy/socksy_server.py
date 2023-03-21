"""


:name: socksy_server
"""

# Standard library imports
import datetime
import logging.config
import os
import sys
import threading
import time
import socket
import random

# Third-party imports
from flask import Flask, request, redirect, render_template
from flask_socketio import SocketIO
import eventlet

# Initialize Flask and SocketIO (must be global)
socksyServer = Flask(__name__)
socksyServer.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(socksyServer)

# Monkey-patch Eventlet (must be global)
eventlet.monkey_patch()

def flask_thread(debug, host, port):
    """


    :param debug: True to enable debug mode in server
    :param host: the ip address of the host
    :param port: the port number to start the server on
    :return: None
    """
    socketio.run(socksyServer, debug=debug, host=host, port=port)


@socketio.on('connect')
def test_connect():
    print("socket connected")

@socketio.on('socksy_authenticate')
def handle_socksy_authenticate(username, password):
    print(f'socksy_authenticate, username: {username}, password: {password}')

@socketio.on('disconnect')
def handle_disconnect():
    print('socket disconnected')

@socketio.on('message')
def handle_message(username, msg, datetime):
    print(f'{username}@{datetime}: {msg}')

@socketio.on('my_message')
def handle_my_message(data):
    print('my_message: ', data)

def test_emit_message():
    print('test_emit_message thread started.')

    while True:
        time.sleep(10 + random.randint(0, 5))
        date_time_now = datetime.datetime.now()
        socketio.emit('message', ('server', date_time_now.strftime('%m/%d/%Y, %H:%M:%S'), f'Here\'s a new int! {random.randint(1, 1024)}'))
        print('message sent')


if __name__ == '__main__':
    print(f'starting Socksy Server...')

    ipAddress = ""

    # Get hostname and ip address
    try:
        hostname = socket.gethostname()
        ipAddress = socket.gethostbyname(hostname)
    except socket.error as e:
        print(e)
        ipAddress = '127.0.0.1'

    hostPort = 6000
    print(f'IP address: \'{ipAddress}:{hostPort}\'')



    testEmitMessageThread = threading.Thread(target=test_emit_message)
    testEmitMessageThread.start()

    # Run Flask app with SocketIO wrapper. Set host with static IP
    flaskApp = threading.Thread(target=flask_thread(True, ipAddress, hostPort))
    flaskApp.start()
