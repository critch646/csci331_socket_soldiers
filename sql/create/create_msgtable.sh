#!/bin/bash

# create Messages table
mysql --host="marie.csci.viu.ca" --database="csci331a_socksy" \
      --user="csci331a" --password="S2L4uv7Z" \
      < "./create/create_msgtable.sql"

#EOF
