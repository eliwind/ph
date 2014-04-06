import redis
import json

from ses_email import sendmail

import util
from datetime import date, timedelta

def sendReminderEmail (email, name, date, shift, config):
    body = '''\
Hello!

This e-mail is your reminder that you are signed up for parent help or snack at Agassiz Preschool:

Shift: %s
Date: %s

Please note that you are responsible for filling your parent help or snack slot.  If you are no longer available, please find a replacement who can take your slot.

If you have any questions, please e-mail %s at %s or call at %s.

Thanks, and enjoy Parent Help!

Your friends at Agassiz Preschool
''' % (shift, date, config['phcName'], config['phcEmail'], config['phcPhone'])

    sendmail (email, 'Agassiz Parent Help or Snack reminder', body)
    
            

if __name__ == '__main__':
    # This runs weekends, early.  So check everything between now and one week from now
    r = redis.StrictRedis()

    config = r.hgetall('config')
    slots = r.zrangebyscore ('slotsbydate', util.toScore(date.today()), util.toScore(date.today() + timedelta(days=7)))
    pipe = r.pipeline()
    for slot in slots:
        pipe.hgetall(slot)

    for shift in pipe.execute():
        if ('worker' in shift):
            worker = json.loads(shift['worker'])
            sendReminderEmail(worker['email'], worker['name'], shift['date'], shift['shift'], config)

