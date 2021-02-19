# Wiser

This is a small personal project, to attempt to get to know Python and AWS DynamoDB better.

The basic flow is:

1) Store the date and time that the script is run (the intention is to graph the information with a maximum resolution of every 15 minutes, and this will be difficult if it isn't consistent)
2) Iterate through all the rooms connected to the Wiser Hub and store in a dictionary (The hub automatically averages if there are multiple devices in a single room, i.e. two TRVs)
3) Retrieve the local temperature and humidity from 'Open Weather Maps' and store in the same dictionary
4) Upload the dictionary to AWS DynamoDB (using 'boto3').

Pre-requisites:
1) A Drayton Wiser heating system
2) An 'Open Weather Maps' API key (free)

Optional:
1) A Google Cloud API key (you could just find your credentials and put them in the gmap.params config file)