__author__ = "Mayur Bhangale"

from lxml import html
import requests
import smtplib
import schedule
import os, time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)


def send_mail(recipient, subject, message):
    username = "your email"
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


def write_to_file(file, data, mode):
    write_file = open(file, mode)
    write_file.write(data)
    write_file.close()


def check():
    try:
        page = requests.get('http://results.unipune.ac.in/')
        tree = html.fromstring(page.content)

        # get text from first row
        latest = str(tree.xpath('//span[@id="ContentPlaceHolder1_dgvResult_lblCourse_0"]//text()')).strip('[]')

        # store latest
        local_data = open('history.txt').read()

        if local_data != latest:
            send_mail('mayurbhangale96@gmail.com', 'SPPU Result Notifier', latest)
            write_to_file('history.txt', latest, 'w')

        else:
            print("No new updates")
    except requests.exceptions.ConnectionError:
        requests.status_code = "Connection refused"


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    phone_number = request.form['phoneNumber']
    write_to_file('users.txt', email + '\n', 'a')  # a is for append
    send_mail(email, "SPPU Results Notifier", "Thank you for registering " + name)

    return render_template(
        'success.html',
        uname=name,
        data=email
    )


@app.route('/', methods=['GET'])
def demo():
    """Demo.html is a template that calls the other routes in this example."""
    return render_template('hello.html', token=session.get('access_token'))


if __name__ == "__main__":
    schedule.every(10).minutes.do(check())
    app.debug = os.environ.get('FLASK_DEBUG', True)
    app.run(port=7000)
