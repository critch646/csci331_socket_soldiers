"""
creates a global variable for the database connection for use in the entire server application
"""
from .servermariadb import DatabaseConnection

dolphin_db = DatabaseConnection()