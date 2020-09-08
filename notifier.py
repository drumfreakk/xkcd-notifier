#!/usr/bin/python

import requests
from sys import argv

latest_file = "/home/kip/.config/polybar/xkcd-notifier/latest"

what = 0

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


latest = int(useFile(latest_file, 'r', '')[0:4])

while True:
	status = requests.get('https://www.xkcd.com/' + str(latest + 1) + '/').status_code

	if status == 200:
		latest += 1
		useFile(latest_file, 'w', str(latest) + 'Unread')

	elif status == 404:
		toPrint = ""

		if useFile(latest_file, 'r', '')[4:] == 'Unread':
			toPrint += "New: "
	
		if argv[1] == "read":
			toPrint = ""
			useFile(latest_file, 'w', str(latest) + 'Read')
		
		toPrint += str(latest)
		print(" " + toPrint)
		break

