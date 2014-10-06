from datetime import datetime

def signup_body (name, date, shift, config):
    return '''\
Hello!

This e-mail confirms that you've signed up for parent help or snack at Agassiz Preschool:

Shift: %s
Date: %s
Who's working: %s    

If you have any questions, please e-mail %s at %s or call at %s.

Thanks!

Your friends at Agassiz Preschool
''' % (shift, pretty_date(date), name, config['phcName'], config['phcEmail'], config['phcPhone'])

def signup_subject (name, date, shift, config):
    return 'Parent Help confirmation: %s on %s' % (shift, pretty_date(date))

def cancel_body (name, date, shift, config):
    return '''\
Hello!

This e-mail confirms that your Agassiz Preschool parent help shift has been canceled:

Shift: %s
Date: %s
Who was working: %s
    
If you have any questions, please e-mail %s at %s or call at %s.

Thanks!

Your friends at Agassiz Preschool
''' % (shift, pretty_date(date), name, config['phcName'], config['phcEmail'], config['phcPhone'])

def cancel_subject (name, date, shift, config):
    return 'Your Parent Help shift has been canceled: %s on %s' % (shift, pretty_date(date))

def reminder_body (name, date, shift, config):
    return '''
Hello!

This e-mail is your reminder that you are signed up for parent help or snack at Agassiz Preschool:

Shift: %s
Date: %s
Who's working: %s    

Please note that you are responsible for filling your parent help or snack slot.  If you are no longer available, please find a replacement who can take your slot.

If you have any questions, please e-mail %s at %s or call at %s.

Thanks, and enjoy Parent Help!

Your friends at Agassiz Preschool
''' % (shift, pretty_date(date), name, config['phcName'], config['phcEmail'], config['phcPhone'])

def reminder_subject (name, date, shift, config):
    return 'Parent Help reminder: %s on %s' % (shift, pretty_date(date))

def announce_body (date, am1, am2, pm, snack, config):
    am1Txt = am1['family'] + ' [' + am1['name'] + ']' if am1 else 'None'
    am2Txt = am2['family'] + ' [' + am2['name'] + ']' if am2 else 'None'
    pmTxt = pm['family'] + ' [' + pm['name'] + ']' if pm else 'None'
    snackTxt = snack['family'] + ' [' + snack['name'] + ']' if snack else 'None'
    return '''
Agassiz Preschool Parent Helpers for %s :

AM1: %s
AM2: %s
PM: %s
Snack: %s

If you have any questions, please e-mail %s at %s or call at %s.
''' % (pretty_print_date(date), am1Txt, am2Txt, pmTxt, snackTxt, config['phcName'], config['phcEmail'], config['phcPhone'])

def announce_subject (date, am1, am2, pm, snack, config):
    return '[Agassiz PH] Today\'s Parent Helpers' 

def pretty_date (date):
    return pretty_print_date(datetime.strptime(date, '%Y-%m-%d'))

def pretty_print_date (date):
    return date.strftime('%A %B %d, %Y')
