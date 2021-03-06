import sys
import urllib2
import json
import os
import csv
import datetime
import time


args = list(sys.argv)[1:]
if len(args) != 4:
	raise Exception("Need 4 arguments: start day, end day, month, and year")

apiURL = 'http://api.wunderground.com/api/41e9482d39e03f1e/history_'
#year = '2017'
#month = '04'
#day = '01'
endURL = '/q/NY/New_York.json'

#f = urllib2.urlopen(apiURL + year + month + day + endURL)
#json_string = f.read()
#parsed_json = json.loads(json_string)
#observations = parsed_json["history"]["observations"]
#for time in observations:
#	hour = time["date"]["hour"]
#	minute = time["date"]["min"]
#	temperature = time["tempi"]
#	print((hour, minute, temperature))

#f.close()

#beginDate = datetime.datetime(2017, 9, 14, 12, 0, 0)

def getTemp2(beginDay, endDay, month, year):
	temperatures = []
	dewpoints = []
	humidity = []
	windspeed = []
	windgust = []
	visibility = []
	pressure = []
	windchill = []
	heatindex = []
	precipitation = []
	timestamps = []
	try:
		os.remove('weatherData.csv')
	except OSError:
		pass
	with open('weatherData.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=' ',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)


		for i in range(beginDay, endDay):

			if (month > 9):
				monthURL = str(month)
			else:
				monthURL = "0" + str(month)
			if (i > 9):
				day = str(i)
			else:
				day = "0" + str(i)
			URL = apiURL + str(year) + monthURL + day + endURL

			f = urllib2.urlopen(apiURL + str(year) + monthURL + day + endURL)
			json_string = f.read()
			parsed_json = json.loads(json_string)
			observations = parsed_json["history"]["observations"]
			for timei in observations:
				yeari = int(timei["date"]["year"])
				monthi = int(timei["date"]["mon"])
				dayi = int(timei["date"]["mday"])
				houri = int(timei["date"]["hour"])
				minutei = int(timei["date"]["min"])
				temperature = float(timei["tempi"])

				dewpoints.append(float(timei["dewpti"]))
				humidity.append(float(timei["hum"]))
				windspeed.append(float(timei["wspdi"]))
				windgust.append(float(timei["wgusti"]))
				visibility.append(float(timei["visi"]))
				pressure.append(float(timei["pressurei"]))
				windchill.append(float(timei["windchilli"]))
				heatindex.append(float(timei["heatindexi"]))
				precipitation.append(float(timei["precipi"]))

				D = datetime.datetime(yeari, monthi, dayi, houri, minutei, 0)
				timestamp = time.strftime("%d-%b-%Y %H:%M:%S", D.utctimetuple())
				temperatures.append(temperature)
				timestamps.append(timestamp)


				#print((hour, minute, temperature))
			f.close()
		spamwriter.writerow(temperatures)
		spamwriter.writerow(dewpoints)
		spamwriter.writerow(humidity)
		spamwriter.writerow(windspeed)
		spamwriter.writerow(windgust)
		spamwriter.writerow(visibility)
		spamwriter.writerow(pressure)
		spamwriter.writerow(windchill)
		spamwriter.writerow(heatindex)
		spamwriter.writerow(precipitation)
	try:
		os.remove('weatherDataTimestamps.csv')
	except OSError:
		pass
	with open('weatherDataTimestamps.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(timestamps)
	print(temperatures)


getTemp2(int(args[0]), int(args[1]), int(args[2]), int(args[3]))








def getTemp1():
	temperatures = [0] * 96 * 30
	year = '2017'
	month = '04'
	day = '01'
	try:
		os.remove('weatherData.csv')
	except OSError:
		pass
	with open('weatherData.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=' ',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)

		tempIndex = 0
		for i in range(1, 31):
			if (i > 9):
				day = str(i)
			else:
				day = "0" + str(i)
			f = urllib2.urlopen(apiURL + year + month + day + endURL)
			json_string = f.read()
			parsed_json = json.loads(json_string)
			observations = parsed_json["history"]["observations"]
			for time in observations:
				if tempIndex >= 96*30:
					continue
				yeari = int(time["date"]["year"])
				monthi = int(time["date"]["mon"])
				dayi = int(time["date"]["mday"])
				houri = int(time["date"]["hour"])
				minutei = int(time["date"]["min"])
				temperature = float(time["tempi"])
				
				minFromStart = (dayi-1)*1440 + houri*60 + minutei
				while tempIndex*15 < minFromStart:
					temperatures[tempIndex] = temperature
					tempIndex += 1

				#print((hour, minute, temperature))
			f.close()
		spamwriter.writerow(temperatures)
	print(temperatures)
