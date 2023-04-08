"""
Creates and configures a Flask SocketIO server instance.

Patches Flask's eventlet

@name: server_socketio
@authors: Zeke Critchlow
@date: 2023/04/08
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