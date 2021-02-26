# Wiser Logging

I like data, I like graphs, and I have 'smart' central heating in my house. After a quick search in Google, I found this [repository](https://github.com/asantaga/wiserHomeAssistantPlatform) and decided that I wanted to do a small personal project to attempt to get to know Python and AWS DynamoDB better. 

## Basic flow:

1) Store the date and time that the script is run (the intention is to graph the information with a maximum resolution of every 15 minutes, and this will be difficult if it isn't consistent)
2) Iterate through all the rooms connected to the Wiser Hub and store in a dictionary (The hub automatically averages if there are multiple devices in a single room, i.e. two TRVs)
3) Retrieve the local temperature and humidity from 'Open Weather Maps' and store in the same dictionary
4) Upload the dictionary to AWS DynamoDB (using 'boto3').

The end goal is to graph the data on a website, but that will be aseperate project.

## Pre-requisites:
1. A Drayton Wiser heating system
2. An AWS account (which includes a certrain number of free Dynamo transactions)
3. An 'Open Weather Maps' API key (free)
4. A tolerance for reading / using code that was written by a complete amateur

## Optional:
1) A Google Cloud API key (you could just find your coordinates and put them in the gmap.params config file)

## Parameter files

At the moment, I've created a seperate parameters file for each external service (i.e. Google, Wiser, Open Weather Maps), just because I wasn't sure of the final structure and it makes it easier to move things around. The format of those files is as follows:

**coords.params**:

Used to store your location, to avoid having to query the Google Maps API every time). You can probably get away with 1 decimal place on the coordinates, but I would use 2 to ensure I get my nearest weather station (Google does it to 5 or 6 DPs.

```
latitude=XX.XXXXXX
longitude=XX.XXXXXX
```

**dynamo.params**:

Used to store your AWS Dynamo credentials. The recommendation would be for a unique IAM account with read and write access to DynamoDB only (this will give the access and secret key. You would then chose whichever AWS region you want to use (You get a large allocation of free transactions, so probably chose the one closest!)

```
aws_access_key=XXXXXXXXXXXXXXXXXXX
aws_secret_access_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
region_name=XXXXXXXXX
```

**gmaps.params**:

Optional, if you intend to get your coordinates this way (I already had the code for another project, so I thoughts I'd include it)

```
key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**owm.params**:

You can create a free account to access the APIs from https://openweathermap.org/. You could easily replace this with another service, but I was struggling to find one that offered current weather conditions for free, with a station near me.
I've used metric units (Centigrade). If you don't specify, it does Kelvin, which isn't terribly helpful in this application. You may have to check the code if you chose anything other °C.

```
appid=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
units=metric
```

**wiser.params**:

If you hven't got a Drayton Wiser system, then  this is all a bit pointless! You can find out how to get your details from [here](https://it.knightnet.org.uk/kb/nr-qa/drayton-wiser-heating-control/#controlling-the-system)

```
wiserkey=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## Running the code on a automatic schedule:

I need to put something here, but you basically setup a cronjob

