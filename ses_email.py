import smtplib
from email.mime.text import MIMEText

def sendmail (toaddr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'eli.daniel@gmail.com'
    msg['To'] = toaddr
    
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP_SSL('email-smtp.us-east-1.amazonaws.com')
    s.login ('AKIAJCX6NGII4NPM2ONA', 'Aho1fIvhLaL368fjxCGfnlD4pIkKLwsyfscxzBRU9FDk' )
    s.sendmail('eli.daniel@gmail.com', toaddr, msg.as_string())
    s.quit()


    
