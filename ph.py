from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for

import redis
import json

from ses_email import sendmail
from smtplib import SMTPRecipientsRefused
from dateutil import rrule


import util
import email_contents

app = Flask(__name__)
r = redis.StrictRedis()

@app.route('/')
def index():
    return redirect(url_for('static', filename='calendar.html'))

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'GET':
        # read the config
        return json.dumps(r.hgetall('config'))

    # set the config
    r.hmset ('config', request.form)
    return json.dumps('success')

@app.route('/shifts')
def shifts():
    family = request.args.get('family')
    slots = r.lrange (family, 0, -1)
    pipe = r.pipeline()
    for slot in slots:
        pipe.hgetall(slot)

    return json.dumps([util.fixWorker(s) for s in pipe.execute()])
    

@app.route('/cancel')
def cancel():
    shift = request.args.get('shift')
    date = request.args.get('date')
    # TODO: make sure all arguments are provided

    # Make sure the shift exists
    shifts = util.getSlots (r, date, shift)
    if len(shifts) == 0:
        return json.dumps('shift not available')
    
    shiftname = shifts[0]['date'] + '|' + shifts[0]['shift']
    worker = json.loads(r.hget(shiftname, 'worker'))
    r.hdel (shiftname, 'worker')
    r.lrem (worker['family'], 0, shiftname)
    config = r.hgetall('config')
    try:
        sendCancelEmail (worker['email'], worker['name'], shifts[0]['date'], shifts[0]['shift'], config)
    except SMTPRecipientsRefused:
        pass # oh well
    return json.dumps('success')


@app.route('/signup')
def signup():
    shift = request.args.get('shift')
    date = request.args.get('date')
    name = request.args.get('name')
    email = request.args.get('email')
    family = request.args.get('family')
    
    # TODO: make sure all arguments are provided

    # Make sure the shift exists
    shifts = util.getSlots (r, date, shift)
    if len(shifts) == 0:
        return json.dumps('shift not available')

    shiftname = shifts[0]['date'] + '|' + shifts[0]['shift']
    oldworker = r.hget(shiftname, 'worker')
    worker = {'name':name, 'email':email, 'family':family}
    if (oldworker):
        oldworker = json.loads(oldworker)
        if oldworker == worker:
            # replacing a worker with the same one; nothing to do
            return json.dumps('success')
        r.lrem (oldworker['family'], 0, shiftname)

    r.hset (shiftname, 'worker', json.dumps(worker))
    r.lpush (family, shiftname)
    config = r.hgetall('config')

    # if this is taking over a shift formerly assigned to someone else, send the old person a cancellation email 
    try:
        if oldworker and oldworker['email'] != email:
            sendCancelEmail (oldworker['email'], oldworker['name'], shifts[0]['date'], shift, config)
    except SMTPRecipientsRefused:
        pass # oh well

    # if this a new shift, or taking over a shift from someone else, send the new person a signup email
    try:
        if not oldworker or oldworker['email'] != email:
            sendSignupEmail (email, name, shifts[0]['date'], shift, config)
    except SMTPRecipientsRefused:
        pass # oh well

    # don't send any emails for just changing details of a shift under the same email address
    return json.dumps('success')


@app.route('/schedule')
def schedule():
    startDate = date.fromtimestamp(request.args.get('start', type=int))
    endDate = date.fromtimestamp(request.args.get('end', type=int))
    # TODO: make sure all arguments are provided

    
    # For each date, we want to find all the shifts, then look up each of them
    slots = r.zrangebyscore ('slotsbydate', util.toScore(startDate), util.toScore(endDate))
    pipe = r.pipeline()
    for slot in slots:
        pipe.hgetall(slot)

    return json.dumps([toCalEvent(e) for e in pipe.execute()])


@app.route('/load_semester')
def load_semester():
    start = datetime.strptime(request.args.get('start'), '%m/%d/%Y')
    end = datetime.strptime(request.args.get('end'), '%m/%d/%Y')
    holidays = [datetime.strptime(t.strip(), '%m/%d/%Y') for t in request.args.getlist('holidays') if t]
    half_days = [datetime.strptime(t.strip(), '%m/%d/%Y') for t in request.args.getlist('half_days') if t]

    print 'holidays: [%s]' % ', '.join(map(str, request.values.getlist('holidays')))
    print 'half days: [%s]' % ', '.join(map(str, request.values.getlist('half_days')))

    for day in rrule.rrule (rrule.DAILY, 
                            byweekday=(rrule.MO,rrule.TU,rrule.WE,rrule.TH,rrule.FR), 
                            dtstart=start, until=end):
        print 'testing day: ' + str(day)
        if day in holidays:
            continue

        for shift in ['AM1', 'AM2', 'Snack']:
            load_shift (day, shift)

        if day in half_days:
            continue

        load_shift (day, 'PM')
    return json.dumps('success')

##############################################################

def sendSignupEmail (email, name, date, shift, config):
    body = email_contents.signup_body(name, date, shift, config)
    subject = email_contents.signup_subject(name, date, shift, config)
    sendmail (email, subject, body)
    
def sendCancelEmail (email, name, date, shift, config):
    body = email_contents.cancel_body(name, date, shift, config)
    subject = email_contents.cancel_subject(name, date, shift, config)
    sendmail (email, subject, body)

def toCalEvent (slot):
    '''Turns a slot as stored in redis into the right JSON format for rendering in FullCalendar'''
    worker = None
    if ('worker' in slot):
        worker = json.loads(slot['worker'])
        title = slot['shift'] + ': ' + worker['family']
        color='#00b4cc'
        textColor='black'
    else:
        title = slot['shift']
        color = '#005f6b'
        textColor='white'
        
    return {
        'title': title,
        'start': slot['date'] + 'T' + util.getStartTime(slot['shift']) + 'Z',
        'end': slot['date'] + 'T' + util.getEndTime(slot['shift']) + 'Z',
        'color': color,
        'textColor': textColor,

        # extra fields to pass through for editing shifts
        'worker':worker,
        'shift':slot['shift']
        }

    
def load_shift (day, shift):
    printdate = day.strftime('%Y-%m-%d')
    numdate = int (day.strftime('%Y%m%d'))
    r.zadd ('slotsbydate', numdate, printdate + '|' + shift)
    r.hset (printdate + '|' + shift, 'shift', shift)
    r.hset (printdate + '|' + shift, 'date', printdate)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
