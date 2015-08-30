import smtplib
import ConfigParser
from email.mime.text import MIMEText

def sendmail (toaddr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'parenthelp@agassizpreschool.org'
    msg['To'] = toaddr
    
    cfg = ConfigParser.ConfigParser()
    cfg.read('ses.cfg')
    
    s = smtplib.SMTP_SSL('email-smtp.us-east-1.amazonaws.com')
    s.login (cfg.get('ses', 'smtp_username', 'BOGUS'),
             cfg.get('ses', 'smtp_password', 'BOGUS'))
    s.sendmail('parenthelp@agassizpreschool.org', toaddr, msg.as_string())
    s.quit()
    
