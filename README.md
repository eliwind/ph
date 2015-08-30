Agassiz Preschool parent help system
==
To set up:

1. Install redis (apt-get install redis-server)
1. Install pip (apt-get install python-pip)
1. Clone this repo into /ph
1. Activate ph virtualenv
1. Run server: python server.py
1. Install crontab to run scheduled jobs
1. Set up SES credentials for email: create a file called ses.cfg in the working directory with the following contents:
```
[ses]
smtp_username: <AWS SMTP username for SES>
smtp_password: <AWS SMTP password for SES>
```


To migrate an existing redis database:

1. on old system, send SAVE command
1. copy dump.rdb to new system
1. make sure appendonlyfile is off, and start redis
1. on new system, send BGREWRITEAOF
1. turn AOF back on
