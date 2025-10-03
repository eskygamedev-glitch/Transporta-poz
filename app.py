import requests
import time


url = "https://saraksti.lv/gpsdata.ashx?gps"
headers = {
    "Origin-Custom": "saraksti.lv"
}
sequence = "2,11,"
def fetch_data():
    response = requests.get(url, headers=headers)
    lines = response.text.split("\n")
    lines = [line for line in lines if line.startswith(sequence)]
    for line in lines:
        a = line.split(",")
        a = a[2:4]
        print("Lat: {}, Lon: {}".format(a[1], a[0]))
        
            
    
while True:
    fetch_data()
    print("Waiting for 10 seconds...")
    time.sleep(10)


# 2 ir autobusi
# 1 trolejbusi
# 3 tramvaji

#24192407(garums WE),56983048 (platums NS)
#a-b (turp)
#b-a (atpakaļ)

