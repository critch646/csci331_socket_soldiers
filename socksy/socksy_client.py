"""


:name: socksy_client
"""

# Standard library imports
import logging.config
import os
import sys
import threading
import time
import socket
import asyncio

# Third-party Imports
import socketio

socketio = socketio.Client()

@socketio.on('my_message')
def on_message(data):
	print('I received a message: ', data)

@socketio.event
def connect():
	print('I am connected!')


@socketio.event
def connect_error(data):
	print('Connection Error: ', data)


def socksy_authenticate(username, password):
	socketio.emit('socksy_authenticate', data=(username, password))

@socketio.event
def disconnect():
	print('Disconnected')





if __name__ == '__main__':
	socketio.connect('http://localhost:6000')
	print('my sid is', socketio.sid)
	socketio.emit('my_message', {'foo': 'bar'})
	username = os.getlogin()
	time.sleep(1)
	socksy_authenticate(username, 'Orange55')

	socketio.disconnect()


