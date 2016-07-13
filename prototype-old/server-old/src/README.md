Hello. To run the server, you need cargo (the rust package manager). You also need a postgre database with a user "server" and a database storeit.
First cd to ./database and execute init_database.sh. Then execute postgre.sh to launch the postgre daemon.

Use cargo run to start the server.

To use the python test script you need at least python 3.5.
