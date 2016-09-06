import json
import web
import cloudserver
from KNNalgo import KNearestNeighbors
from trainingData import training

urls = (
"/","BeaconVals")
class generateTrainingData:
    trainingData = []
    trainingLabels = []
    def generate(self):
        rooms = ["nwc4", "nwc7", "nwc8", "nwc10", "nwc10m", "nwc1000m_a1", "nwc1000m_a2", "nwc1000m_a3", "nwc1000m_a4", "nwc1000m_a5", "nwc1000m_a6", "nwc1000m_a7", "nwc1000m_a8", "nwc1003b", "nwc1003g","nwc1006", "nwc1007", "nwc1008", "nwc1009", "nwc1010", "nwc1003b_t", "nwc1003b_a", "nwc1003b_b", "nwc1003b_c"]
        infile = "backup2.txt"
        f = open(infile, 'r')
        x = f.readlines()
        for i in range(len(x)):
            y = x[i].split('\t')
            last = y[-1].split('\n')
            y[-1] = last[0]
            y = map(int, y)
            self.trainingData.append(y)

        infile = "backuplabels2.txt"
        f = open(infile, 'r')
        x = f.readlines()
        for j in range(len(x)):
            y = x[j]
            last = y.split('\n')
            y = last[0]
            self.trainingLabels += [rooms.index(y)]

class BeaconVals:
    trainingDataGenerator = generateTrainingData()
    trainingDataGenerator.generate()
    points = trainingDataGenerator.trainingData
    labels = training.labelNames
    labelNumber = trainingDataGenerator.trainingLabels
    KNN = KNearestNeighbors(11, points, labelNumber)
    sortedRoomList = ["nwc4", "nwc7", "nwc8", "nwc10", "nwc10m", "nwc1000m_a1", "nwc1000m_a2", "nwc1000m_a3", "nwc1000m_a4", "nwc1000m_a5", "nwc1000m_a6", "nwc1000m_a7", "nwc1000m_a8", "nwc1003b", "nwc1003g","nwc1006", "nwc1007", "nwc1008", "nwc1009", "nwc1010", "nwc1003b_t", "nwc1003b_a", "nwc1003b_b", "nwc1003b_c"]

    def POST(self):

        
        raw_data=web.data()
        locs = raw_data.split(',')
        l = locs[1:]
        ID = locs[0]
        locs = map(int, l)
        KNN = KNearestNeighbors(11, points, labelNumber)
        location = KNN.classifier(locs)


        #username = cloudserver.db.userIDLookup(ID)
        #if (username is not None):
        #    alpha = username.split('_')
        #    if (len(alpha >= 1)):
        #        if (alpha[0] == "alpha"):
        #            ID = "9432F0A3-660D-4C35-AA63-C7CFDD6D0F4D"
        #            location = cloudserver.db.getUserLocation(ID)


        cloudserver.db.ReportLocationAssociation(ID, self.labels[location])
        cloudserver.db.SaveLocationData(0, self.labels[location])
        moveUsers = cloudserver.SE.moveUsers
        changeScheduleUsers = cloudserver.SE.changeScheduleUsers
        turnOffApplianceUsers = cloudserver.SE.turnOffApplianceUsers
        synchronizeApplianceUsers = cloudserver.SE.synchronizeApplianceUsers

        balance_server = cloudserver.db.getUserBalance(cloudserver.db.userIDLookup(ID))



        if (balance_server == False):
            balance_server = 0
        json_return={
            "location":"Location Name",
            "location_id":"locationIDString",
            "balance":balance_server,
            "suggestions":[]
        }
        def make_suggestion_item(iType, iTitle, iBodyText, iReward, messageID, inotification=0, Others={}):
            Others.update({
                "type":iType,
                "title":iTitle,
                "body":iBodyText,
                "reward":iReward,
                "notification":inotification,
                "messageID":messageID
                })
            return Others

        json_return["location_id"]=self.labels[location]
        json_return["location"]=cloudserver.db.RoomIdToName(self.labels[location])
        #keys = turnOffApplianceUsers.keys()
        #for i in range(len(keys)):
        #    json_return["debug"].append(keys[i])
        if (ID in moveUsers.keys()):
            roomInfo = moveUsers[ID]
            roomId=roomInfo["roomDest"]
            roomName=cloudserver.db.RoomIdToName(roomId)
            messageID = roomInfo["messageID"]

            title="Move to "+roomName
            body="Please consider sharing the room to lower everyone's energy footprint."
            reward=4
            json_return["suggestions"].append(
                make_suggestion_item("move",title,body,reward, messageID,0, {"to":roomName,"to_id":roomId})
            )

        #json_return["debug"] = turnOffApplianceUsers
        if (ID in turnOffApplianceUsers.keys()):
            applianceList = turnOffApplianceUsers[ID]
            for appliance in applianceList:
                applianceID = appliance["id"]
                applianceName = appliance["name"]
                powerUsage = appliance["value"]
                messageID = "{0}|{1}|{2}".format("turnoff", ID, applianceID)
                if (powerUsage <= 0):
                    continue
                title="Shut off "+applianceName
                body=applianceName+" is consuming excess power (" + str(powerUsage) + " watts), please see if you can switch off some appliance."
                reward=1
                doPush=0
                if(powerUsage>100):
                    #!!TODO: make doPush=1,2,3,4 according to various criteria, not a single threshold.
                    doPush=1
                json_return["suggestions"].append(
                    make_suggestion_item("turnoff",title, body, reward, messageID, doPush, {"appl":applianceName,"appl_id":applianceID, "power":powerUsage}))


                #applianceID="nwc1003b_c_plug"
                #applianceName=cloudserver.db.ApplIdToName(applianceID)
                #title="Shut off "+applianceName+"?"
                #pwr=cloudserver.db.ApplIdToVal(applianceID)
                #body=applianceName+" is consuming excess power ("+pwr+" watts), please see if you can switch off some appliance."
                #reward=int(0.1*pwr)+1
                #json_return["suggestions"].append(
                #    make_suggestion_item("turnoff",title,body,reward,{"appl":applianceName,"appl_id":applianceID, "power":pwr})
                #    )

        #filter out message using suggestionIDs
        #Check 1: if display timestamp indicates a recent "dismiss", remove the message entirely.
        #TODO: personalize the interval
        interval=20*60
        sinceTime=cloudserver.db._now()-interval
        json_return["suggestions"]=[
            item for item in json_return["suggestions"]
            if cloudserver.db.pushManagementDispCheck(item["messageID"], sinceTime) is True #not passed the ckeck->recently dismissed
        ]
        #Check 2: if push timeout is too short, erase the push flag.
        #TODO: personalized push interval from DB (notification frequency in config)
        pushInterval=60*60 # !!!! TESTINT ONLY ### should be >= than display timeout anyway
        pushSinceTime=cloudserver.db._now()-pushInterval
        for i in range(len(json_return["suggestions"])):
            if json_return["suggestions"][i]["notification"]!=0:
                #this is a push message; check if we want to push
                messageID=json_return["suggestions"][i]["messageID"]
                if cloudserver.db.pushManagementPushCheck(messageID, pushSinceTime)==False: #last notification too recent
                    #erase flag
                    json_return["suggestions"][i]["notification"]=0
                else: #good to go
                    #remember this push, do not repeat.
                    cloudserver.db.pushManagementPushUpdate(messageID)

        return cloudserver.db._encode(json_return,False)

    def GET(self):
        result = cloudserver.db.QueryLocationData(0)
        return result

Beacons = web.application(urls, locals());
