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

def pretty_date (date):
    return datetime.strptime(date, '%Y-%m-%d').strftime('%A %B %d, %Y')
