#!/usr/bin/env python

"""
tgs_collate_twitch_json.py
Collate multiple twich JSONs into two CSVs.
"""

import sys
import json
import csv
import glob
import urllib.request 
from datetime import datetime
from time import strftime

def process_time(t):
	dt = t.split("_")
	dt[1] = dt[1][:2] + ":" + dt[1][2:4] + ":" + dt[1][4:]
	return dt

if len(sys.argv) > 1:
	#If there's a game_name we use it
	game_name = sys.argv[1]
else:
	#otherwise we use Binding of Isaac (because it's awesome)
	game_name = 'The%20Binding%20of%20Isaac%3A%20Rebirth'
decoded_game_name = urllib.request.unquote(game_name)

#Glob works like unix ls command - really cool!
file_list = glob.glob("*|"+game_name+".json")

if len(file_list) == 0:
	raise ValueError("No JSON files available for %s." % decoded_game_name)
print("%i JSON files found for %s." % (len(file_list),decoded_game_name))

#Open the two CSV files. One for the game level stats, 
# another for streamer level stats.
game_csv     = csv.writer(open(game_name+"_game_stats.csv",'wt+'))
streamer_csv = csv.writer(open(game_name+"_streamer_stats.csv",'wt+'))

#Initialize the game_csv with headers
game_csv.writerow([
	"date", 
	"time",
	"total_streamers",
	"partner_streamers",
	"total_viewers",
	"average_viewers",
	"max_viewers",
	"min_viewers",
	"average_fps",
	"max_fps",
	"min_fps",
	"average_followers",
	"max_followers",
	"min_followers"])

streamer_csv.writerow([
	"date",
	"time",
	"stream_id",
	"streamer_name",
	"viewers",
	"top_stream",
	"average_fps",
	"language",
	"lifetime_followers",
	"lifetime_views"])

for i,f_n in enumerate(file_list):
	#We use enumerate to know which file we're on.

	#game_row will be used for game-level stats
	game_row = []
	print("--------------------------------")

	#Pull out the date_time to use for each row.
	date_time = f_n.split("|")[0]
	game_row.append(process_time(date_time)[0])
	game_row.append(process_time(date_time)[1])
	print("File %i of %i: %s at %s." % (i+1,len(file_list),process_time(date_time)[0],process_time(date_time)[1])) 

	#Parse the json file into a dictionary.
	f = open(f_n)
	data = json.load(f)
	f.close()

	#All the streamers are held under 'streams'
	streams = data['streams']

	#The total streams is just the length of streams.
	total_streams = data['_total']
	game_row.append(total_streams)
	print("Total streams: %i" % total_streams)

	#Look under channel->partner to see if the streamers are partners.
	partner_streamers = [1 if s['channel']['partner'] else 0 for s in streams]
	total_partners = sum(partner_streamers)
	game_row.append(total_partners)
	print("Total partners: %i" % total_partners)

	#Looks at the viewership.
	viewerships = [s['viewers'] for s in streams]
	#Work out the total viewers for the game
	total_viewers = sum(viewerships)
	game_row.append(total_viewers)
	print("Total viewers: %i" % total_viewers)
	#Also the average viewers per stream.
	average_viewers = total_viewers/total_streams
	game_row.append(average_viewers)
	print("Average viewers: %i" % average_viewers)
	#And the max/min viewers
	max_viewers = max(viewerships)
	min_viewers = min(viewerships)
	game_row.append(max_viewers)
	game_row.append(min_viewers)
	print("Max viewers: %i" % max_viewers)
	print("Min viewers: %i" % min_viewers)

	#Look at the average fps per stream, averaged for the game.
	average_fpses = [s['average_fps'] for s in streams]
	average_fps = sum(average_fpses)/len(average_fpses)
	game_row.append(average_fps)
	print("Average FPS: %i" % average_fps)
	#Also look at the max and min averages.
	max_fps = max(average_fpses)
	min_fps = min(average_fpses)
	game_row.append(max_fps)
	game_row.append(min_fps)
	print("Max FPS: %i" % max_fps)
	print("Min FPS: %i" % min_fps)

	#Look under channel->followers to see the streamers' followers.
	followers = [s['channel']['followers'] for s in streams]
	#Calculate the average followers per stream
	average_followers = sum(followers)/len(followers)
	game_row.append(average_followers)
	print("Average Followers: %i" % average_followers)
	#Also look at the max and min followers
	max_followers = max(followers)
	min_followers = min(followers)
	game_row.append(max_followers)
	game_row.append(min_followers)
	print("Max followers: %i" % max_followers)
	print("Min followers: %i" % min_followers)

	#Write all this data to the game_csv.
	game_csv.writerow(game_row)

	#Now we cycle through the streamers and log them in the streamer_csv
	for j,s in enumerate(streams):
		stream_row = []

		stream_row.append(process_time(date_time)[0])
		stream_row.append(process_time(date_time)[1])
		stream_row.append(s['_id'])
		stream_row.append(s['channel']['display_name'])
		stream_row.append(s['viewers'])

		if s['viewers'] == max_viewers:
			print("********************")
			print("Max viewership for %s at %s: %i viewers on channel %s." % (process_time(date_time)[0],process_time(date_time)[1],max_viewers, s['channel']['display_name']))
			print("********************")
			stream_row.append(True)
		else:
			stream_row.append(False)

		stream_row.append(s['average_fps'])
		stream_row.append(s['channel']['language'])
		stream_row.append(s['channel']['followers'])
		stream_row.append(s['channel']['views'])

		streamer_csv.writerow(stream_row)



