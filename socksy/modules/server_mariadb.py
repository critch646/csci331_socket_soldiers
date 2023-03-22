# Module Imports
import mariadb
import sys
from dotenv import load_dotenv


class DatabaseConnection:

    # prepared statements for inserting data
    add_msg_stmt = "INSERT INTO Messages (userID, content, sentAt) VALUES (?,?,?)"
    add_usr_stmt = "INSERT INTO Users (username, permissionLevel) VALUES (?,?)"

    def __int__(self, envfile):

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

    def add_message(self, user_id, content, sent_at):
        """INSERT INTO Messages (userID, content, sentAt) VALUES (?,?,?)"""
        self.cur.execute(self.add_msg_stmt, (user_id, content, sent_at))

    def add_user(self, username, permission_level):
        """INSERT INTO Users (username, permissionLevel) VALUES (?,?)"""
        self.cur.execute(self.add_usr_stmt, (username, permission_level))
