#!/usr/bin/env python2
import smtplib
from email.mime.text import MIMEText
# Just a quick mock-up for sending a simple email.


msg = MIMEText("This is a test of the emergency SMTP notification system.") #body
msg['Subject'] = "Demo test subject"
msg['From'] = 'device@acme.local'
msg['To'] = 'some1@email.com'

snd = smtplib.SMTP('mail.example.com') #SMTP server
snd.sendmail(msg['From'], msg['To'], msg.as_string())
snd.quit()
