#!/usr/bin/env python

"""
tgs_analyze_game_csv.py
Analyse the game CSV file.
"""

import sys
from datetime import datetime
from time import strftime
import urllib.request 

import pandas as pd
import numpy as np

if len(sys.argv) > 1:
	#If there's a game_name we use it
	game_name = sys.argv[1]
else:
	#otherwise we use Binding of Isaac (because it's awesome)
	game_name = 'The%20Binding%20of%20Isaac%3A%20Rebirth'
decoded_game_name = urllib.request.unquote(game_name)

file_name = game_name + "_game_stats.csv"

game_data = pd.read_csv(file_name)

print(game_data.sort(['total_viewers'],ascending=False)[['date','time','total_viewers','total_streamers']])