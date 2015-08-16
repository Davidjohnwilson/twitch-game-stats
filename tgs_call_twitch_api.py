#!/usr/bin/env python

"""
tgs_call_twitch_api.py
Call the twich API for a game listed in the command line arguments.
Saves results in a time stamped JSON file.
"""

import sys
import requests
import json
import urllib.request 
from datetime import datetime
from time import strftime

if len(sys.argv) > 1:
	#If there's a game_name we use it
	game_name = sys.argv[1]
else:
	#otherwise we use Binding of Isaac (because it's awesome)
	game_name = 'The%20Binding%20of%20Isaac%3A%20Rebirth'

base_url = 'https://api.twitch.tv/kraken/search/streams?type=live&limit=1000'
base_url += '&q=' + game_name

#Make the call to the API
r = requests.get(base_url)

#Extract the JSON data
json_data = r.json()

print("Total of %s streams are streaming %s." % (json_data['_total'],urllib.request.unquote(game_name)))

#Time stamp the filename
filename = datetime.now().strftime("%Y-%m-%d_%H%M%S") 
filename += "_" + game_name + ".json"

with open(filename,'w') as file:
	json.dump(json_data, file)
