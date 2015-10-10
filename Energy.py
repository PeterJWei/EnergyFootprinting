
import web

urls = (
"/(.+)/SavePlug","SavePlug", #raw values: watts, kwh
"/(.+)/SaveHVAC","SaveHVAC",  #raw values: pressure+temp
"/(.+)/SaveLight","SaveLight" #raw values: on or off / watts
)

class SaveHVAC:
    def POST(self,room):
        pass
        return 0
    def GET(self,room):
        return "{0}".format(room)
class SaveLight:
    def POST(self,room):
        pass
        return 0


class SavePlug:
    def POST(self,room):
        raw_data = web.data() # you can get data use this method
        data=json.loads(raw_data)

        description=data["name"]
        energy=data["energy"]
        power=data["power"]
        db.SavePlug(room,description,energy,power)

        return "200 OK"
EnergyReport = web.application(urls, locals())
