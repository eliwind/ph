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

    startDate = request.args.get('start', type=int)
    endDate = request.args.get('end', type=int)
    # TODO: make sure all arguments are provided

    
    # For each date, we want to find all the shifts, then look up each of them
    slots = r.zrangebyscore ('slotsbydate', startDate, endDate)

    pipe = r.pipeline()
    for slot in slots:
        pipe.hgetall(slot)

    return render_template('schedule.html',
                           results=pipe.execute(),
                           start=startDate,
                           end=endDate,
                           json=json)




if __name__ == '__main__':
    app.run(host='0.0.0.0')
