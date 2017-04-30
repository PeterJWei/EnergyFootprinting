import DBScrape
import csv
import os
import argparse
import calendar
import datetime
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--start", help="how many days back to start scrape", type=int)
parser.add_argument("-e", "--end", help="how many days back to end scrape", type=int)
parser.add_argument("-o", "--offset", help="how many hours to offset scrape", type=int)
args = parser.parse_args()


#set defaults
end = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
start = calendar.timegm(datetime.datetime.utcnow().utctimetuple())-24*60*60 #1 day
hours = 0
if (args.start):
	start = calendar.timegm(datetime.datetime.utcnow().utctimetuple())-24*60*60*args.start
if (args.end):
	end = calendar.timegm(datetime.datetime.utcnow().utctimetuple())-24*60*60*args.end
assert(start < end)

if (args.offset):
	start += 60*60*args.offset
	end += 60*60*args.offset


try:
    os.remove('userSnapshots.csv')
except OSError:
    pass

db=DBScrape.DBScrape()

users = db.registration_col1()
shots = db.snapshots_col_users(start, end)

with open('userSnapshots.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
	writeArray = []
	for person in users:
		personID = person["name"]
		writeArray.append(personID)

	for shot in shots:
		userList = shot["data"]
		writeArray = []
		for person in users:
			userFound = False
			personID = person["userID"]
			if user in userList:
				writeArray.append(userList[user]["value"])
				userFound = True
				continue
			if (not userFound):
				writeArray.append(0)

		spamwriter.writerow(writeArray)
