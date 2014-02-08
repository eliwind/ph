from datetime import date
from flask import Flask
from flask import render_template
from flask import request

import redis
import json

app = Flask(__name__)


@app.route('/signup')
def signup():
    r = redis.StrictRedis()

    shift = request.args.get('shift')
    date = request.args.get('date')
    name = request.args.get('name')
    email = request.args.get('email')
    # TODO: make sure all arguments are provided

    # Make sure the shift exists
    slots=r.zrangebyscore ('slotsbydate', date, date)
    pipe = r.pipeline()
    for slot in slots:
        pipe.hgetall(slot)
    shifts = filter (lambda x: x['shift'] == shift,
                     pipe.execute())
    if len(shifts) >= 1:
        r.hset (shifts[0]['date'] + '|' + shifts[0]['shift'],
                'worker', json.dumps({'name':name, 'email':email}))
        return render_template ('signup.html', success=True, name=name, email=email, shift=shift, date=date)

    elif len(shifts) == 0:
        return render_template ('signup.html', success=False, err='Shift not available', name=name, email=email, shift=shift, date=date)

    

@app.route('/schedule')
def schedule():
    r = redis.StrictRedis()

    startDate = date.fromtimestamp(request.args.get('start', type=int))
    endDate = date.fromtimestamp(request.args.get('end', type=int))
    # TODO: make sure all arguments are provided

    
    # For each date, we want to find all the shifts, then look up each of them
    slots = r.zrangebyscore ('slotsbydate', toScore(startDate), toScore(endDate))

    pipe = r.pipeline()
    for slot in slots:
        pipe.hgetall(slot)

    calevents = [toCalEvent(e) for e in pipe.execute()]
    return json.dumps(calevents)


##############################################################

def toScore (date):
    '''Converts a date to an integer to use as a score in a redis sorted set: YYYYMMDD'''
    return int (date.strftime('%Y%m%d'))

def toCalEvent (slot):
    '''Turns a slot as stored in redis into the right JSON format for rendering in FullCalendar'''
    if ('worker' in slot):
        title = slot['shift'] + ': ' + json.loads(slot['worker'])['name']
        color='#00b4cc'
        textColor='black'
    else:
        title = slot['shift']
        color = '#005f6b'
        textColor='white'
        
    return {
        'title': title,
        'start': slot['date'] + 'T' + getStartTime(slot['shift']) + 'Z',
        'end': slot['date'] + 'T' + getEndTime(slot['shift']) + 'Z',
        'color': color,
        'textColor': textColor
        }

def getStartTime (shift):
    '''Gets start times for each type of shift'''
    return {
        'AM1':'08:30:00',
        'AM2':'08:30:00',
        'PM':'12:30:00',
        'Snack':'08:30:00'
        }[shift]

def getEndTime (shift):
    '''Gets end times for each type of shift'''
    return {
        'AM1':'13:00:00',
        'AM2':'13:00:00',
        'PM':'14:20:00',
        'Snack':'09:00:00'
        }[shift]
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
