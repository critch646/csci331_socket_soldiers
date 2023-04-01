"""
Creates and configures a Flask SocketIO server instance.

@name: server_socketio
"""

from flask import Flask
from flask_socketio import SocketIO


# Initialize Flask and SocketIO (must be global)
socksyServer = Flask(__name__)
socksyServer.config['SECRET_KEY'] = 'secret!'
socketio_server = SocketIO(socksyServer)

import eventlet
# Monkey-patch Eventlet (must be global)
eventlet.monkey_patch()