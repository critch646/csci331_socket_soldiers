# Module Imports
import mariadb
import sys
import datetime
from datetime import date

from dotenv import load_dotenv


class DatabaseConnection:

    # prepared statements for inserting data
    # INSERT STATEMENTS
    add_msg_stmt = "INSERT INTO Messages (userID, content, sentAt) VALUES (?,?,?)"
    add_usr_stmt = "INSERT INTO Users (username, permissionLevel) VALUES (?,?)"

    # UPDATE STATEMENTS
    make_user_admin_stmt = "UPDATE Users SET permissionLevel = ? WHERE username = ?"

    # SELECT STATEMENTS
    fullpull_msg_stmt = "SELECT userID, content, sentAt FROM Messages ORDER BY sentAt ASC"
    specpull_msg_stmt = "SELECT userID, content, sentAt FROM Messages WHERE sentAt > ? ORDER BY sentAt ASC"

    def __int__(self):
        # load information from the ENV file
        load_dotenv('../dolphin.env')

        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')
        HOST = os.getenv('HOST')
        DATABASE = os.getenv('DATABASE')

        try:
            self.conn = mariadb.connect(
                user=USERNAME,
                password=PASSWORD,
                host=HOST,
                database=DATABASE)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self.cur = conn.cursor()

    def add_message(self, user_id: str, content: str, sent_at):
        """
        :param user_id: string containing the unique identifier for the user
        :param content: string containing the message sent by the user
        :param sent_at: formatted datetime string to be inserted into the database
        :return: None
        """
        self.cur.execute(self.add_msg_stmt, (user_id, content, sent_at))

    def add_user(self, username: str) -> None:
        """
        :param username: string containing the unique identifier for the user
        :return: None
        """
        self.cur.execute(self.add_usr_stmt, username)

    def change_user_perms(self, username: str, permission_level: int) -> None:
        """
        :param username: string containing the unique identifier for the user
        :param permission_level: int pertaining to the level of permission that the user will be granted
        :return: None
        """
        try:
            if (permission_level < 1) or (permission_level > 5):
                raise ValueError
            else:
                self.cur.execute(self.make_user_admin_stmt, (permission_level, username))
                print(f"user: {username} permission level changed to: {permission_level}")
        except ValueError:
            print(f"ValueError: provided value = {permission_level} ... value must be between 1 and 5 (inclusive)")

    def pull_message_history(self, days=-1):
        """
        :param days: number of days in the past from the current date that we want to look back on, defaults to -1
        :return: cursor object with the result set contained within it
        """

        # if no date is specified, we want to perform a full pull (entire history)
        if days == -1:
            self.cur.execute(self.fullpull_msg_stmt)
        else:
            # determines date we need to trace back to
            today = str(date.today()).split('-')                                            # grabs current date
            formatted_date = datetime.date(int(today[0]), int(today[1]), int(today[2]))     # formats current date for arithmetic
            time_difference = datetime.timedelta(days)                                      # formats time difference
            past_date = formatted_date - time_difference                                    # performs subtraction
            past_date = past_date.strftime('%m/%d/%Y, %H:%M:%S')                            # formats the date for db use

            self.cur.execute(self.specpull_msg_stmt, past_date)

            result_set = self.cur
            return result_set



