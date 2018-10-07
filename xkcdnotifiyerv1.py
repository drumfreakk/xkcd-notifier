import requests
from time import sleep
import smtplib
from email.message import EmailMessage

what = 1990
times = 0

# def useFile(doc, manner, write):
#     manners = ['r', 'a', 'w', 'w+']
#     if manner in manners:
#         f = open(doc, manner)
#         if manner == 'r':
#             doc = f.read()
#             f.close()
#             return doc
#         else:
#             f.write(write)
#             f.close()
#     else:
#         return "Invalid manner"

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

while True:
    # what = int(useFile('./latest.txt', 'r', ''))
    status = test()
    print(what)
    print(status)
    if status == 200:
        what += 1
        times = 0
    if status == 404:
        if times == 0:
            sendMail('kieran.houtgraaf@gmail.com', 'There is a new xkcd comic!', 'https://www.xkcd.com/' + str(what - 1) + '\n(And possibly more...)')
            # useFile('./latest.txt', 'w', what)
            times = 1
        sleep(43200)
