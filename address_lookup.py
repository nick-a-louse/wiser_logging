import urllib.request, urllib.parse, urllib.error
import json
import ssl
import os
#-----------API keys-----------

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
#abs_file_path = os.path.join(script_dir, 'gmap.params')

with open(os.path.join(script_dir, 'gmap.params'), "r") as f:
    gmaps = f.read().split("\n")
google_key = ""

for lines in gmaps:
    line = lines.split("=")
    if line[0] == "key":
        google_key = line[1]


#-----------API endpoint-----------
gserviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

#-----------Ignore SSL certificate errors-----------
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_coordinates(address):

        #-----------Retrieve address details from Google Geocode APIs-----------
    parms = dict()
    parms['address'] = address
    parms['key'] = google_key
    url = gserviceurl + urllib.parse.urlencode(parms)

        #-----------print('Retrieving', url)-----------
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', end = "\r\n")
    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)

        #-----------Add location to the database-----------

    latitude = js['results'][0]['geometry']['location']['lat']
    longitude = js['results'][0]['geometry']['location']['lng']

    return (latitude, longitude)


