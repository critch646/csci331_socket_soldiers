#!/bin/bash

# drop Users table
mysql --host="marie.csci.viu.ca" --database="csci331a_socksy" \
      --user="csci331a" --password="S2L4uv7Z" \
      < "./destroy/destroy_usertable.sql"

#EOF