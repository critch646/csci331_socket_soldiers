#!/bin/bash

# create mock data for Users table
mysql --host="marie.csci.viu.ca" --database="csci331a_socksy" \
      --user="csci331a" --password="S2L4uv7Z" \
      < "./create/mock_userdata.sql"

# create mock data for Messages table
mysql --host="marie.csci.viu.ca" --database="csci331a_socksy" \
      --user="csci331a" --password="S2L4uv7Z" \
      < "./create/mock_msgdata.sql"

#EOF