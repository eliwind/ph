import redis
import json

r = redis.StrictRedis()
r.flushdb()

# load legal shifts
for month in [1, 3, 5, 7] :
    for day in range (1, 32) :
        printdate = '2014-' + '{0:0>2}'.format(month) + '-' + '{0:0>2}'.format(day)
        for shift in ['AM1', 'AM2', 'PM', 'Snack']:
            r.zadd ('slotsbydate', int('2014'+'{0:0>2}'.format(month)+'{0:0>2}'.format(day)), printdate +'|' + shift)
            r.hset (printdate + '|' + shift, 'shift', shift)
            r.hset (printdate + '|' + shift, 'date', printdate)

# load a few signups
signups = [
    {'worker': {'name':'Eli Daniel',
              'email':'eli.daniel@gmail.com'},
     'date': '2014-01-10',
     'shift': 'AM1'},
    
    {'worker': {'name': 'Joe Blow',
              'email':'jblow@gmail.com'},
     'date': '2014-01-12',
     'shift': 'AM1'},
    
    {'worker': {'name':'Jane Blew',
              'email':'jblew@gmail.com'},
     'date': '2014-01-12',
     'shift': 'AM2'},
    
    {'worker': {'name':'Bob McFrob',
              'email':'mcfrob@gmail.com'},
     'date': '2014-01-15',
     'shift': 'Snack'}]
 
for i in signups:
    r.hset (i['date']+'|'+i['shift'],
            'worker',
            json.dumps ({'name': i['worker']['name'],
                         'email': i['worker']['email']}))

