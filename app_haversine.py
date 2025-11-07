import requests
import time
import math

def fetch_data():
    response = requests.get(url, headers=headers)
    lines = response.text.split("\n")
    lines = [line for line in lines if line.startswith(sequence)]


    for line in lines:
        a = line.split(",")

        #parbaudei
        if len(a) < 5:
            continue


        vir = str(a[8])
        # micro gradi
        lon_mikro = float(a[2])
        lat_mikro = float(a[3])

        # pareja
        lon = lon_mikro / 1000000
        lat = lat_mikro / 1000000

        print(f"Lat: {lat:.6f}, Lon: {lon:.6f}, Virziens: {vir}")

        # atrast tuvako/esoso pieturu
        match = trySearch(lat, lon)
        if match is not None:
            print(f"Autobuss atrodas pieturā: {match}")
        


url = "https://saraksti.lv/gpsdata.ashx?gps"
headers = {
    "Origin-Custom": "saraksti.lv"
}





# parbaudei(vai ir pieturaa)

def haversine(lat1, lon1, lat2, lon2):
    R = 6363133  # Zemes radiuss(metros)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def trySearch(lat, lon):
    MAX_DISTANCE_METERS = 30
    closest_stop = None
    closest_distance = float("inf")  

    for stop in all_bus_stops:
        stop_name, stop_lat, stop_lon = stop
        distance = haversine(lat, lon, stop_lat, stop_lon)
        if distance < closest_distance:
            closest_distance = distance
            closest_stop = stop_name


    if closest_distance <= MAX_DISTANCE_METERS:
        print(f"Atrasta atbilstība: {closest_stop} ({closest_distance:.1f} m attālumā)")
        return closest_stop
    else:
        print(f"Tuvāko {MAX_DISTANCE_METERS} m attālumā nav pieturu (tuvākā: {closest_stop} {closest_distance:.1f} m)")
        return None





all_bus_stops = [
    ["sarkandaugava_station_bus_stop_a_b", 56.99569, 24.12903],
    ["sarkandaugava_bus_stop_a_b", 56.99419, 24.12494],
    ["sarkandaugava_bus_stop_b_a", 56.99487, 24.12679],
    ["tilta_iela_bus_stop_b_a", 56.99232, 24.12559],
    ["tilta_iela_bus_stop_a_b", 56.99287, 24.12413],
    ["vitolu_iela_bus_stop_b_a", 56.99232, 24.12559],
    ["vitolu_iela_bus_stop_a_b", 56.99287, 24.12413],
    ["olaines_iela_bus_stop_b_a", 56.98653, 24.13385],
    ["olaines_iela_bus_stop_a_b", 56.98733, 24.133],
    ["traumatologijas_bus_stop_a_b", 56.98378, 24.13604],
    ["traumatologijas_bus_stop_b_a", 56.98292, 24.13627],
    ["laktas_iela_bus_stop_a_b", 56.97934, 24.13657],
    ["laktas_iela_bus_stop_b_a", 56.9783, 24.13601],
    ["ierednu_iela_bus_stop_a_b", 56.97434, 24.13557],
    ["ierednu_iela_bus_stop_b_a", 56.97332, 24.13517],
    ["eveles_iela_bus_stop_a_b", 56.97069, 24.1333],
    ["eveles_iela_bus_stop_b_a", 56.96898, 24.13173],
    ["palidzibas_iela_bus_stop_b_a", 56.96474, 24.12758],
    ["bruninieku_iela_bus_stop_a_b", 56.96093, 24.1217],
    ["bruninieku_iela_bus_stop_b_a", 56.96178, 24.12284],
    ["emelngaila_iela_bus_stop_b_a", 56.95923, 24.11856],
    ["raina_bulvaris_bus_stop_b_a", 56.95393, 24.10927],
    ["central_tirgus_bus_stop_a_b", 56.94572, 24.11878],
    ["centrala_stacija_bus_stop_a_b", 56.94755, 24.11816],
    ["centrala_stacija_bus_stop_b_a", 56.94607, 24.1187],
    ["merkela_iela_bus_stop_a_b", 56.94908, 24.11928],
    ["inzenieru_iela_bus_stop_a_b", 56.95122, 24.11682],
    ["inzenieru_iela_bus_stop_b_a", 56.9509, 24.1149],
    ["makslas_muzejs_bus_stop_a_b", 56.95565, 24.11133],
    ["makslas_muzejs_bus_stop_b_a", 56.95611, 24.11258],
    ["lacplesa_iela_bus_stop_a_b", 56.95818, 24.11688],
    ["lacplesa_iela_bus_stop_b_a", 56.94978, 24.13127],
    ["francu_licejs_bus_stopa_a_b", 56.96357, 24.12596],
    ["aloju_iela_bus_stopa_a_b", 56.96757, 24.13079]
]

delta = 0.0001
sequence = "1,3,"

while True:
   
    fetch_data()
#    trySearch(56.95122, 24.11682)
    # findMatch(56.96357, 24.12596)

    print("Waiting for 10 seconds...")
    print("\n")
    time.sleep(10)


# 2 ir autobusi
# 1 trolejbusi
# 3 tramvaji

#24192407(garums WE),56983048 (platums NS)
#a-b (no centra)

#b-a (uz centru)
