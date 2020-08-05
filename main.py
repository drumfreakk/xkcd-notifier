import os
import requests
from time import sleep, strftime
import smtplib
from email.message import EmailMessage
import sys

os.chdir('/home/' + sys.argv[1] + '/xkcd-notifier')

sender_email = "email.to.send.from@email.com"
sender_email_password = "password"
reciever_email = "email.to.send.to@email.com"

what = 1990
times = 0
done = 0

###################################################
# use files

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

###################################################

try:

###################################################
# send mails

	def sendMail(toaddr, subject, body):
		msg = EmailMessage()
		msg.set_content(body)

		msg['Subject'] = subject
		msg['From'] = sender_email
		msg['To'] = toaddr

		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.starttls()
		s.login(sender_email, sender_email_password)
		s.send_message(msg)
		s.quit()

###################################################


###################################################
# test xkcd

	def test():
		r = requests.get('https://www.xkcd.com/' + str(what) + '/')
		return r.status_code

###################################################


###################################################
# main loop

	what = int(useFile('latest', 'r', '')[0:4])

	while True:
		status = test()
		print(str(strftime('%Y-%m-%d %H:%M:%S')) + ' XKCD no.: ' + str(what) + ' Status: ' + str(status))

		if useFile('latest', 'r', '')[4:] == 'Internet':
			sendMail(reciever_email, 'Internet Error', 'On one ore more runs there was no internet connection, causing it to error. Check the logs for more details.')
			print(str(strftime('%Y-%m-%d %H:%M:%S')) + ' Internet error resolved')

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
					sendMail(reciever_email, 'There is a new xkcd comic! We are up to ' + str(what - 1) + '!', 'https://www.xkcd.com/' + str(what - 1))	

				else:
					sendMail(reciever_email, 'There is a new xkcd comic! We are up to ' + str(what - 1) + '!', 'https://www.xkcd.com/' + str(what - 1) + '\n(And ' + str(done) + ' more...)')

			useFile('latest', 'w', str(what) + 'True')
			done = 0
			quit()

		else:
			sendMail(reciever_email, 'Error?', 'Non-200 or 404 status code: ' + str(status))
			quit()

###################################################

except requests.exceptions.ConnectionError:
	print(str(strftime('%Y-%m-%d %H:%M:%S')) + ' Failed due to no internet connection.')
	useFile('latest', 'w', str(what) + 'Internet')

