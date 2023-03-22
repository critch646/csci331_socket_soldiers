#!/bin/bash

# runs both drop-table scripts

echo "dropping Messages table"
sh ./destroy/destroy_msgtable.sh
echo "dropping Users table"
sh ./destroy/destroy_usertable.sh

#EOF