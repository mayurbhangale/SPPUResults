#!/usr/bin/env python

from lxml import html
import requests
import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from flask import Flask, render_template, request, session
from pyscheduler import schedule

app = Flask(__name__)

def send_mail(recipient, subject, message):
    username = "mayurbhangale@live.com"
    password = "feelfoul92702689"

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


def write_to_file(file, data, mode):
    write_file = open(file, mode)
    write_file.write(data)
    write_file.close()


# check for results every 5 minutes
@schedule('*/1 * * * *')
def check():
    try:
        page = requests.get('http://results.unipune.ac.in/')
        tree = html.fromstring(page.content)

        # get text from first row
        latest = str(tree.xpath('//span[@id="ContentPlaceHolder1_dgvResult_lblCourse_0"]//text()')).strip('[]')

        # store latest
        local_data = open('history.txt').read()
        lines = open('users.txt').read().splitlines()

        if local_data != latest:
            write_to_file('history.txt', latest, 'w')
            for email_id in lines:
                send_mail(email_id, '[BOT] SPPU Results out!', 'Result for ' + latest + ' announced.')
        else:
            print("No new updates")
    except requests.exceptions.ConnectionError:
        requests.status_code = "Connection refused"


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']

    if email in open('users.txt').read():
        return render_template(
            'already.html',
            uname=name,
            data=email
        )

    else:
        write_to_file('users.txt', email + '\n', 'a')  # a is for append
        send_mail(email, "[BOT] SPPU Results Notifier", "Thank you for registering " + name)

        return render_template(
            'success.html',
            uname=name,
            data=email
        )


@app.route('/', methods=['GET'])
def demo():
    return render_template('index.html', token=session.get('access_token'))


if __name__ == "__main__":
    app.debug = os.environ.get('FLASK_DEBUG', True)
    app.run(port=7001)