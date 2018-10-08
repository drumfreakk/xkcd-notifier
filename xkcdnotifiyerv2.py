import os
import requests
from time import sleep, strftime
import smtplib
from email.message import EmailMessage

os.chdir('/home/pi/xkcd-notifier')

what = 1990
times = 0
done = 0

def useFile(doc, manner, write):
    manners = ['r', 'a', 'w', 'w+']
    if manner in manners:
        f = open(doc, manner)
        if manner == 'r':
            doc = f.read()
            f.close()
            return doc
        else:
            f.write(write)
            f.close()
    else:
        return "Invalid manner"

def sendMail(toaddr, subject, body):
    msg = EmailMessage()
    msg.set_content(body)

    msg['Subject'] = subject
    msg['From'] = 'xkcdnotifications@gmail.com'
    msg['To'] = 'kieran.houtgraaf@gmail.com'

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('xkcdnotifications@gmail.com', "LekkereKippenBoutjes!")
    s.send_message(msg)
    s.quit()

def test():
    r = requests.get('https://www.xkcd.com/' + str(what) + '/')
    return r.status_code

what = int(useFile('latest', 'r', '')[0:4])
while True:
    status = test()
    print(str(strftime('%Y-%m-%d %H:%M:%S')) + ' XKCD no.: ' + str(what) + ' Status: ' + str(status))
    if status == 200:
        what += 1
        if times == 0:
            useFile('latest', 'w', str(what) + 'False')
            times = 1
        else:
            done += 1
    elif status == 404:
        if useFile('latest', 'r', '')[4:] == 'False':
            if done == 0:
                sendMail('kieran.houtgraaf@gmail.com', 'There is a new xkcd comic! We are up to ' + str(what - 1) + '!', 'https://www.xkcd.com/' + str(what - 1))
            else:
                sendMail('kieran.houtgraaf@gmail.com', 'There is a new xkcd comic! We are up to ' + str(what - 1) + '!', 'https://www.xkcd.com/' + str(what - 1) + '\n(And ' + str(done) + ' more...)')
                useFile('latest', 'w', str(what) + 'True')
        done = 0
        quit()
    else:
        sendMail('kieran.houtgraaf@gmail.com', 'Error?', 'Non-200 or 404 status code: ' + str(status))
        quit()
