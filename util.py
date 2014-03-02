from datetime import date
import redis
import json


def getSlots (r, date, shift):
    '''Gets the slot, if any, for a given date (as YYYYMMDD integer) and shift'''
    slots = r.zrangebyscore ('slotsbydate', date, date)
    pipe = r.pipeline()
    for slot in slots:
        pipe.hgetall(slot)
        
    return [x for x in pipe.execute() if x['shift'] == shift]

def toScore (date):
    '''Converts a date to an integer to use as a score in a redis sorted set: YYYYMMDD'''
    return int (date.strftime('%Y%m%d'))

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

def fixWorker (shift):
    ''' Replaces 'worker' field as json string with an object'''
    if ('worker' in shift):
        shift['worker'] = json.loads(shift['worker'])
    return shift

