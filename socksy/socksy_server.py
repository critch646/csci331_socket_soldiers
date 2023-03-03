"""


:name: socksy_server
"""

# Standard library imports
import logging.config
import os
import sys
import threading
import time
import socket

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


if __name__ == '__main__':
	print(f'starting Socksy Server...')

	# Get hostname and ip address
	hostname = socket.gethostname()
	ipAddress = socket.gethostbyname(hostname)
	hostPort = 6000
	print(f'Hostname: {hostname} with IP address: {ipAddress}')

	# Run Flask app with SocketIO wrapper. Set host with static IP
	flaskApp = threading.Thread(target=flask_thread(
		True, ipAddress, hostPort))
	flaskApp.start()
