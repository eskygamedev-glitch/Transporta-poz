import requests
import time

def fetch_data():
    response = requests.get(url, headers=headers)
    f_response = APIformat(response)
    for transport in f_response:
        match = findMatch(float(transport[3])/1000000, float(transport[2])/1000000, transport[8]) # Transport 8 is bus stop, 3 is Latitude, 2 is Longitude,
    if match != None:
        print("Match found: {}".format(match))

def findMatch(lat, lon, direction):
    for stop in all_bus_stops:
        if ((lat - delta) < stop[2] < (lat + delta)) and ((lon - delta) < stop[3] < (lon + delta)) and direction == stop[1]:
            return stop[0]
    return None

def removeIntigers(str):
    outputStr = ""
    for char in str:
        if char in invalidChars: # Invalid chars can be found below bus stops
            pass
        else:
            outputStr += char
    return outputStr

def APIformat(input):
    lines = input.text.split("\n")
    lines = [line for line in lines if line.startswith(sequence)]
    toreturn = []
    for line in lines:
        splitLine = line.split(",")
        coords = splitLine[2:4]
        splitLine.insert(8, removeIntigers(splitLine[8]))
        splitLine.pop(9)
        print("Lat: {}, Lon: {}, Way: {}".format(coords[1], coords[0], splitLine[8]))
        toreturn.append(splitLine)
    return toreturn
    


all_bus_stops = [
["sarkandaugava_station_bus_stop_a_b", "a-b", 56.99569, 24.12903],
["sarkandaugava_bus_stop_a_b", "a-b", 56.99419, 24.12494],
["sarkandaugava_bus_stop_b_a", "b-a", 56.99487, 24.12679],
["tilta_iela_bus_stop_b_a", "b-a", 56.99232, 24.12559],
["tilta_iela_bus_stop_a_b", "a-b", 56.99287, 24.12413],
["vitolu_iela_bus_stop_b_a", "b-a", 56.99232, 24.12559],
["vitolu_iela_bus_stop_a_b", "a-b", 56.99287, 24.12413],
["olaines_iela_bus_stop_b_a", "b-a", 56.98653, 24.13385],
["olaines_iela_bus_stop_a_b", "a-b", 56.98733, 24.133],
["traumatologijas_bus_stop_a_b", "a-b", 56.98378, 24.13604],
["traumatologijas_bus_stop_b_a", "b-a", 56.98292, 24.13627],
["laktas_iela_bus_stop_a_b", "a-b", 56.97934, 24.13657],
["laktas_iela_bus_stop_b_a", "b-a", 56.9783, 24.13601],
["ierednu_iela_bus_stop_a_b", "a-b", 56.97434, 24.13557],
["ierednu_iela_bus_stop_b_a", "b-a", 56.97332, 24.13517],
["eveles_iela_bus_stop_a_b", "a-b", 56.97069, 24.1333],
["eveles_iela_bus_stop_b_a", "b-a", 56.96898, 24.13173],
["palidzibas_iela_bus_stop_b_a", "b-a", 56.96474, 24.12758],
["bruninieku_iela_bus_stop_a_b", "a-b", 56.96093, 24.1217],
["bruninieku_iela_bus_stop_b_a", "b-a", 56.96178, 24.12284],
["emelngaila_iela_bus_stop_b_a", "b-a", 56.95923, 24.11856],
["raina_bulvaris_bus_stop_b_a", "b-a", 56.95393, 24.10927],
["central_tirgus_bus_stop_a_b", "a-b", 56.94572, 24.11878],
["centrala_stacija_bus_stop_a_b", "a-b", 56.94755, 24.11816],
["centrala_stacija_bus_stop_b_a", "b-a", 56.94607, 24.1187],
["merkela_iela_bus_stop_a_b", "a-b", 56.94908, 24.11928],
["inzenieru_iela_bus_stop_a_b", "a-b", 56.95122, 24.11682],
["inzenieru_iela_bus_stop_b_a", "b-a", 56.9509, 24.1149],
["makslas_muzejs_bus_stop_a_b", "a-b", 56.95565, 24.11133],
["makslas_muzejs_bus_stop_b_a", "b-a", 56.95611, 24.11258],
["lacplesa_iela_bus_stop_a_b", "a-b", 56.95818, 24.11688],
["lacplesa_iela_bus_stop_b_a", "b-a", 56.94978, 24.13127],
["francu_licejs_bus_stopa_a_b", "a-b", 56.96357, 24.12596],
["aloju_iela_bus_stopa_a_b", "a-b", 56.96757, 24.13079],
]

url = "https://saraksti.lv/gpsdata.ashx?gps"
headers = {
    "Origin-Custom": "saraksti.lv"
}


delta = 0.0002
sequence = "1,3,"
invalidChars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


while True:
   
    fetch_data()

    
    print("Waiting for 10 seconds...")
    time.sleep(10)


# 2 ir autobusi
# 1 trolejbusi
# 3 tramvaji

#24192407(garums WE),56983048 (platums NS)
#a-b (no centra)

#b-a (uz centru)


# karoc tas butu sigh.... spilto domuzimi (a-b) un tad tu dabu orginu un destination. 1. ir orgins, 2. destinations, un tu to dabu kaa listu.