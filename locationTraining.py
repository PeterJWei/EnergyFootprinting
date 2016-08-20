import json
import web
import cloudserver
from KNNalgo import KNearestNeighbors
from trainingData import training

urls = (
"/","train")

class train:
    points = training.datapoints
    labels = training.labelNames
    labelNumber = training.labelNumber
    KNN = KNearestNeighbors(3, points, labelNumber)
    rooms = ["nwc10", "nwc10m", "nwc1000m_a1", "nwc1000m_a2", "nwc1000m_a3", "nwc1000m_a4", "nwc1000m_a5", "nwc1000m_a6", "nwc1000m_a7", "nwc1000m_a8", "nwc1003b", "nwc1003g","nwc1006", "nwc1007", "nwc1008", "nwc1009", "nwc1010", "nwc1003b_t", "nwc1003b_a", "nwc1003b_b", "nwc1003b_c", "nwc7", "nwc8"]
    def POST(self):
        raw_data=web.data()
        locs = raw_data.split(',')
        l = locs[1:]

        if (locs[0] == "GET"):
            locs = map(int, l)
            K = KNearestNeighbors(3, cloudserver.trainingData, cloudserver.trainingLabels)
            location = K.classifier(locs)
            return self.rooms[location]
        
        ID = locs[0]
        intID = int(ID)
        locs = map(int, l)
        cloudserver.trainingData.append(locs)
        cloudserver.trainingLabels.append(intID)
        return "success"

    def GET(self):
        result = cloudserver.db.QueryLocationData(0)
        return result

locationTraining = web.application(urls, locals());