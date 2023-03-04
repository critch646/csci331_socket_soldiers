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

import socketio

sio = socketio.Client(logger=True, engineio_logger=True)
sio.connect('http://127.0.1.1:6000')

sio.emit('message', {'from': 'client'})



@sio.on('response')
def response(data):
    print(data)  # {'from': 'server'}

    sio.disconnect()
    exit(0)

