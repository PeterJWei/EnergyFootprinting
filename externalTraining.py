import json
import web
import cloudserver

urls = ("/", "externalTraining")

class externalTraining:
	def POST(self):
		raw_data=web.data()
		locs = raw_data.split(',')
		beaconData = locs[1:]
		beaconString = ""
		if (locs[0] == "NEW"):
			outfile = "newData.txt"
			outfile1 = "newDataLabels.txt"
			f = open(outfile, "a+")
			f1 = open(outfile1, "a+")
			for i in range(len(beaconData))
				beaconString += beaconData[i]
				if (i != (len(beaconData)-1)):
					beaconString += "\t"
		print(beaconString)
		f.writeline(beaconString)
		f1.writeline(locs[0])

		f.close()
		f1.close()


externalLocationTraining = web.application(urls, locals());