import web
import json
import os
import datetime
import pymongo

import blog
import DBMgr
import Energy
import Location
import Query
urls = (
    "/api/EnergyReport",Energy.EnergyReport,
    "/api/LocationReport",Location.LocationReport, #room ID, +(timestamp)?
    "/api/Query",Query.query, #room ID + time range
    "/frontend/(.+)", "frontend",
    "/(.+)/index","index"

)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)



#client = pymongo.MongoClient()
#client = pymongo.MongoClient('localhost', 27017)
#db = client.test_database
db=DBMgr.DBMgr()

render = web.template.render('templates/')


class index:
    def GET(self, path):
        if path=="":
            return "Hello world from bitbucket! this is the icsl energy foot-print api; try out /api/query/room/* "
        print "{0}".format(path)
        return "Energy foot-print"



        #return "Hello {0}".format(name)
class frontend:
    def GET(self,person):
        
        result = db.QueryPerson(person,0,2**31)
        #data=json.dumps(result)
	data=DateTimeEncoder().encode(result) 
        return render.chart(data)
class room:
    def GET(self,room):
        input=str(web.input())
        print input
        print room

        #return input+" {0}".format(name)
        return db.QueryRoom(room,0,2**32)




class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))
def notfound():
    return web.notfound("404 Not Found")

    # You can use template result like below, either is ok:
    #return web.notfound(render.notfound())
    #return web.notfound(str(render.notfound()))
def run():
    app = MyApplication(urls, globals())
    app.notfound = notfound
    app.run(port=8000)
