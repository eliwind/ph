Agassiz Preschool parent help system
==
To set up:

# Install redis (apt-get install redis-server)
# Instally pip (apt-get install python-pip)
# Clone this repo into /ph
# Run server: python server.py
# Install crontab to run scheduled jobs

To migrate an existing redis database:
# on old system, send SAVE command
# copy dump.rdb to new system
# make sure appendonlyfile is off, and start redis
# on new system, send BGREWRITEAOF
# turn AOF back on
