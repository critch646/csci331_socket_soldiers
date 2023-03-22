#!/bin/bash

# runs both create-table scripts

echo "creating Users table"
sh ./create/create_usertable.sh
echo "creating Messages table"
sh ./create/create_msgtable.sh

#EOF