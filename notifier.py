__author__ = "Mayur Bhangale"

from lxml import html
import requests
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_mail(recipient, subject, message):
    username = "your email address"
    password = "your password"

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    print('sending mail to ' + recipient + ' on ' + subject)

    mailServer = smtplib.SMTP('smtp-mail.outlook.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    mailServer.sendmail(username, recipient, msg.as_string())
    mailServer.close()

page = requests.get('http://results.unipune.ac.in/')
tree = html.fromstring(page.content)

#get text from first row
latest = str(tree.xpath('//span[@id="ContentPlaceHolder1_dgvResult_lblCourse_0"]//text()')).strip('[]')

#store latest
local_data = open('history.txt').read()

send_mail('mayurbhangale96@gmail.com', 'SPPU Result Notifier', 'Thanks for subscribing!')

if local_data != latest:
    send_mail('mayurbhangale96@gmail.com', 'SPPU Result Notifier', latest)
    write_file = open('history.txt', 'w')
    write_file.write(latest)
    write_file.close()

else:
    print "No new updates"

