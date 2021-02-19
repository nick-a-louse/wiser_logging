import json
from datetime import datetime
from wiserHeatingAPI import wiserHub
import boto3
from decimal import Decimal
from address_lookup import get_coordinates
from owm import get_station
import logging
import os

#_LOGGER = logging.getLogger(__name__)
#_LOGGER.setLevel(logging.DEBUG)

logging.basicConfig(filename='wiser.log', level=logging.DEBUG)

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]

#------------------ Storing the data and time that the script is run ------------------

now = datetime.now()
d = now.strftime("%Y-%m-%d")
t = now.strftime("%H:%M")

#------------------ Get Wiser Parameters from keyfile ------------------

# To get the wiser hub key, follow the instructions here https://github.com/asantaga/wiserheatingapi

with open(os.path.join(script_dir, "wiser.params"), "r") as f:
    data = f.read().split("\n")
wiserkey = ""
wiserip = ""

for lines in data:
    line = lines.split("=")
    if line[0] == "wiserkey":
        wiserkey = line[1]
    if line[0] == "wiserhubip":
        wiserip = line[1]

wh = wiserHub.wiserHub(wiserip, wiserkey)

print("\n Wiser Hub Details:\n    Wiser Hub IP= {} \n    WiserKey= {}".format(wiserip, wiserkey))

#------------------ Retrieve Room Temperatures ------------------

# Creates a dictionary object called 'data' and then loops through each room (as defined by the Drayton system itself) and to create a json-esque structure in the dictionary 

data = {'room_data': None, 'outside_data': None}

try:
    rooms = {}
    for room in wh.getRooms():
        smartValves = room.get("SmartValveIds")
        if smartValves is None:
            print("Room {} has no smartValves")
        else:
            r = {'set_point': Decimal(room.get("CurrentSetPoint")/10).quantize(Decimal("1.0")),'calculated_temp': Decimal(room.get("CalculatedTemperature")/10).quantize(Decimal("1.0"))} #The boto3 uploader needs the numbers to be converted to a decimal
            if r['set_point'] == Decimal('-20.0'): #-20.0 means 'turned off' so converting the value to null to clarity
                r.update({'set_point': None})
            rooms[room.get("Name")] = r 
    data["room_data"] = rooms

except json.decoder.JSONDecodeError as ex:
    print("JSON Exception")
    logging.error('Unable to retrieve Wiser heating files')

#------------------ Retrieve Outside Temperature ------------------

# Outside temperate will affect the termperature of different rooms in the house. It's also interesting to compare :)

coordinates = list()
station_id = list()

# To get the outside temperature, we first need to know where the user is. The below will check for a user's coordinates.

try:
    with open(os.path.join(script_dir, "coords.params"), "r") as c:
        coords = c.read().split("\n")
    for lines in coords:
        line = lines.split("=")
        if line[0] == "latitude":
            coordinates.append(line[1])
        if line[0] == "longitude":
            coordinates.append(line[1])
    c.close()
    print("\nCoordinates file found:\n    Latitude: " + coordinates[0] + ", Longitude: " + coordinates[1])

# If the coordinates file doesn't exist, or is empty, then it will be created / populated. Needs a Google API account (or to be manually created).

except:
    print("\nNo coordinate file available\n")
    logging.info('No coordinate file available')
    address = (input('Please enter your address:')).lower()
    coordinates = get_coordinates(address)
    with open(os.path.join(script_dir, "coords.params"), "w") as c:
        c.write("latitude="+str(coordinates [0])+"\nlongitude="+str(coordinates [1]))
        c.close()
    print("\nCoordinates file created\n    Latitude: " + str(coordinates [0]) + ", Longitude: " + str(coordinates [0]))
    

# Take the coordinates and get the temperature information from Open Weather Maps

outside_data_raw = get_station(coordinates)

data["outside_data"] = {'outside_temp': Decimal(outside_data_raw[0]).quantize(Decimal("1.0")),'outside_hum': Decimal(outside_data_raw[1]).quantize(Decimal("1"))} #The boto3 uploader needs the numbers to be converted to a decimal

#------------------ Get DynamoDB Parameters from keyfile ------------------

with open(os.path.join(script_dir, "dynamo.params"), "r") as f:
    dyndb = f.read().split("\n")
aws_access_key_id = ""
aws_secret_access_key = ""
aws_region_name = ""


for lines in dyndb:
    line = lines.split("=")
    if line[0] == "aws_access_key_id":
        aws_access_key_id = line[1]
    if line[0] == "aws_secret_access_key":
        aws_secret_access_key = line[1]
    if line[0] == "region_name":
       aws_region_name = line[1]
#print("\nDynamoDB Connection Details:\n    AWS access key id = {} \n    AWS secret access key = {} \n    AWS region = {}\n\n".format(aws_access_key_id, aws_secret_access_key, aws_region_name))

#------------------ Upload data to DynamoDB ------------------

#Each dictionary entry in 'Item' will form a column in the DB. date and time are mandatory in this use case (as they are the keys)

dynamodb = boto3.resource('dynamodb',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region_name)
table = dynamodb.Table('Wiser')

response = table.put_item(
    Item={
        'date': d,
        'time': t,
        'temp_data': data,
    }
)

print('\n\nData uploaded to Dynamo DB')