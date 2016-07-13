#! /bin/bash

echo "JOIN $1 $2 $(./produce_dummy_tree.py dummy_tree) $(cat CRLR.txt)" | nc localhost 7641 &&
nc -l $2
