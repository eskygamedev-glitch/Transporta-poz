import requests
import time


url = "https://saraksti.lv/gpsdata.ashx?gps"
headers = {
    "Origin-Custom": "saraksti.lv"
}

response = requests.get(url, headers=headers)

print(response.text)