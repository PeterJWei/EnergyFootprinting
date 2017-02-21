import web
import cloudserver

urls = ("/", "appSupport",
"/localization/", "userLocalizationAPI")

class appSupport:
	def GET(self):
		data = web.input(id=None)
		if cloudserver.db.userIDLookup(data.id) == None :
			return "Invalid userID"
		else:
			print "user found"
			location = cloudserver.db.getUserLocation(data.id)
			print location
			ret = cloudserver.db.calculateEnergyFootprint(location)
		return ret

class userLocalizationAPI:
	def GET(self):
		return cloudserver.db.getUserLocalizationAPI()
appURL = web.application(urls, locals());