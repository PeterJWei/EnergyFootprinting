import DBScrape



class roomAnalytics:
	energyDictionary = {}
	def roomData(self):
		databaseScrape = DBScrape.DBScrape()
		t = (2017, 4, 1, 0, 0, 0, 0, 0, 0)
		beginTime = calendar.timegm(datetime.datetime.utcfromtimestamp(time.mktime(t)).utctimetuple())
		for i in range(0, 60):
			start = beginTime + i*24*60*60
			end = beginTime + (i+1)*24*60*60
			shots = databaseScrape.snapshots_col_appliances(start, end)

			for snapshot in shots:
				timestamp = snapshot["timestamp"]
				print(timestamp-start)
				return
				data = snapshot["data"]
				for appliance in data:
					params = data[appliance]
					energy = params["value"]
					rooms = params["rooms"]
					for room in rooms:
						if room not in self.energyDictionary:
							self.energyDictionary[room] = [[0]*96 for index in range(60)]

