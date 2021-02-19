import urllib.request, urllib.parse, urllib.error
import json
import os

#-----------API keys-----------:

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]

with open(os.path.join(script_dir, "owm.params"), "r") as f:
    data = f.read().split("\n")

owm_key = ""
units = ""

for lines in data:
    line = lines.split("=")
    if line[0] == "appid":
        owm_key = line[1]
    if line[0] == "units":
        units = line[1]
        


#-----------API endpoint-----------
owmserviceurl = "http://api.openweathermap.org/data/2.5/weather?"

#-----------Building Open Weather Maps URL, and retrieving the JSON-----------

def get_station (coordinates):

    while True:
        #-----------Setting up the parameters to create the concatenated url-----------
        owm = dict()
        owm['lat'] = coordinates[0]
        owm['lon'] = coordinates[1]
        owm['appid'] = owm_key
        owm['units'] = units
        owm_url = owmserviceurl + urllib.parse.urlencode(owm)

        weather = urllib.request.urlopen(owm_url)
        weather_raw = weather.read().decode()
        
        try:
            weather_json = json.loads(weather_raw)
        except:
            print ('No station found')
            break
        
        return (weather_json["main"]["temp"], weather_json["main"]["humidity"])
        break
