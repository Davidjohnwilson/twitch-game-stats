#!/usr/bin/env python

"""
tgs_collate_twitch_json.py
Collate multiple twich JSONs into two CSVs.
"""

import sys
import json
import glob
import urllib.request 
from datetime import datetime
from time import strftime

if len(sys.argv) > 1:
	#If there's a game_name we use it
	game_name = sys.argv[1]
else:
	#otherwise we use Binding of Isaac (because it's awesome)
	game_name = 'The%20Binding%20of%20Isaac%3A%20Rebirth'
decoded_game_name = urllib.request.unquote(game_name)

file_list = glob.glob("*|"+game_name+".json")

if len(file_list) == 0:
	raise ValueError("No JSON files available for %s." % decoded_game_name)
print("%i JSON files found for %s." % (len(file_list),decoded_game_name))

for i,f in enumerate(file_list):
	print(f.split("|")[0]) 
