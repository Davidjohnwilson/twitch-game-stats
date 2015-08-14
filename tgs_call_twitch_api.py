import requests
import json
from datetime import datetime
from time import strftime

game_name = 'The%20Binding%20of%20Isaac%3A%20Rebirth'

base_url = 'https://api.twitch.tv/kraken/search/streams?type=live&limit=1000'
base_url += '&q=' + game_name

r = requests.get(base_url)

json_data = r.json()

print("Total of %s streams are streaming BoI:R." % json_data['_total'])

filename = datetime.now().strftime("%Y-%m-%d_%H%M%S") + "_" + game_name + ".json"

with open(filename,'w') as file:
	json.dump(json_data, file)
