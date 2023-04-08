"""
creates a global variable for the database connection for use in the entire
server application

@name: server_db_connect.py
@authors: Brandon Stanton
@date: 2023/04/08
"""
from .servermariadb import DatabaseConnection

dolphin_db = DatabaseConnection()