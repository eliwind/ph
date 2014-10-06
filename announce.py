import redis
import json

from ses_email import sendmail

import util
import email_contents

from datetime import date, timedelta

def sendAnnounceEmail (shifts, config):
    am1Worker = None
    am2Worker = None
    pmWorker = None
    snackWorker = None

    for s in shifts:
        if 'worker' in s:
            if s['shift'] == 'AM1':
                am1Worker = json.loads(s['worker'])
            elif s['shift'] == 'AM2':
                am2Worker = json.loads(s['worker'])
            elif s['shift'] == 'PM':
                pmWorker = json.loads(s['worker'])
            elif s['shift'] == 'Snack':
                snackWorker = json.loads(s['worker'])
    
    body = email_contents.announce_body(date.today(), am1Worker, am2Worker, pmWorker, snackWorker, config)
    subject = email_contents.announce_subject(date.today(), am1Worker, am2Worker, pmWorker, snackWorker, config)
    sendmail ('ph-alert@agassizpreschool.org', subject, body)

if __name__ == '__main__':
    r = redis.StrictRedis()

    config = r.hgetall('config')
    slots = r.zrangebyscore ('slotsbydate', util.toScore(date.today()), util.toScore(date.today()))
    pipe = r.pipeline()
    for slot in slots:
        pipe.hgetall(slot)

    sendAnnounceEmail (pipe.execute(), config)

