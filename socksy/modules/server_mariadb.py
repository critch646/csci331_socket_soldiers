# Module Imports
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="csci331a",
        password="S2K4uv7Z",
        host="marie.csci.viu.ca",
        port=3306,
        database="csci331a_socksy"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()