import redis
import json

from ses_email import sendmail

import util
import email_contents

from datetime import date, timedelta

def sendReminderEmail (email, name, date, shift, config):
    body = email_contents.reminder_body(name, date, shift, config)
    subject = email_contents.reminder_subject(name, date, shift, config)
    sendmail (email, subject, body)

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

