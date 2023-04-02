# Module Imports
import mysql.connector as mariadb
import os
import sys
import datetime
from datetime import date

from dotenv import load_dotenv
from .chat_data import Message, User


class DatabaseConnection:
    def __init__(self):
        # load information from the ENV file
        load_dotenv('dolphin.env')

        # prepared statements for inserting data
        # INSERT STATEMENTS
        self.add_msg_stmt = "INSERT INTO Messages (username, content) VALUES (%s,%s)"
        self.add_usr_stmt = "INSERT INTO Users (username) VALUES (%s)"
        self.check_user_exists_stmt = "SELECT username FROM Users WHERE username = %s"

        # UPDATE STATEMENTS
        self.make_user_admin_stmt = "UPDATE Users SET permissionLevel = %s WHERE username = %s"

        # SELECT STATEMENTS
        self.fullpull_msg_stmt = "SELECT content, username, sentAt FROM Messages ORDER BY sentAt ASC"
        self.specpull_msg_stmt = "SELECT content, username, sentAt FROM Messages WHERE sentAt > %s ORDER BY sentAt ASC"

        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')
        HOST = os.getenv('HOST')
        DATABASE = os.getenv('DATABASE')

        try:
            self.connection = mariadb.connect(
                user=USERNAME,
                password=PASSWORD,
                host=HOST,
                database=DATABASE)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # assign the object's cursor
        self.cursor = self.connection.cursor(buffered=True)

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def add_message(self, user_id, content):
        """
        :param user_id: string containing the unique identifier for the user
        :param content: string containing the message sent by the user
        :param sent_at: formatted datetime string to be inserted into the database
        :return: None
        """

        self.cursor.execute(self.add_msg_stmt, [user_id, content])
        self.connection.commit()

    def check_user_exists(self, username) -> bool:
        """
        Checks if a given username string exists in the database
        :param username: the string pertaining to the user's username
        :return: TRUE if exists, FALSE if not
        """

        self.cursor.execute(self.check_user_exists_stmt, [username])
        self.cursor.fetchall()

        if self.cursor.rowcount == 0:
            return False
        else:
            return True

    def add_user(self, user: str) -> None:
        """
        :param user: string containing the unique identifier for the user
        :return: None
        """

        self.cursor.execute(self.add_usr_stmt, [user])
        self.connection.commit()

    def change_user_perms(self, user: User, permission_level: int) -> None:
        """
        :param username: string containing the unique identifier for the user
        :param permission_level: int pertaining to the level of permission that the user will be granted
        :return: None
        """
        try:
            if (permission_level < 1) or (permission_level > 5):
                raise ValueError
            else:
                self.cursor.execute(self.make_user_admin_stmt, [permission_level, user.name])
                print(f"user: {user.name} permission level changed to: {permission_level}")
        except ValueError:
            print(f"ValueError: provided value = {permission_level} ... value must be between 1 and 5 (inclusive)")

    def pull_message_history(self, days=-1) -> list:
        """
        :param days: number of days in the past from the current date that we want to look back on, defaults to -1
        :return: cursor object with the result set contained within it
        """

        # if no date is specified, we want to perform a full pull (entire history)
        if days == -1:
            self.cursor.execute(self.fullpull_msg_stmt)
        else:
            # determines date we need to trace back to
            today = str(date.today()).split('-')                                            # grabs current date
            formatted_date = datetime.date(int(today[0]), int(today[1]), int(today[2]))     # formats current date for arithmetic
            time_difference = datetime.timedelta(days)                                      # formats time difference
            past_date = formatted_date - time_difference                                    # performs subtraction
            past_date = past_date.strftime('%m/%d/%Y, %H:%M:%S')                            # formats the date for db use

            self.cursor.execute(self.specpull_msg_stmt, [past_date])

        messagehistory = self.cursor.fetchall()

        messagelist = []

        for item in messagehistory:
            user = User(item[1], "", True)
            newmsg = Message(item[0], user, item[2].strftime('%m/%d/%Y, %H:%M:%S'))
            messagelist.append(newmsg)

        return messagelist


