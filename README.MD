# Twitch Game Stats

This package is intended to collate together details about a single game on Twitch over a series of times. 

It consists of the following files:

* `tgs_call_twitch_api.py`: a python script to call the Twitch API for a particular game (given as a command line argument) and save the results in a time-stamped JSON object. 
* `tgs_collate_twitch_json.py`: a python script to combine a collection of JSON files into two CSVs corresponding to game-level stats and channel-level stats. The only command line argument is the game title: it will find all JSON files for that game in the current directory and collate them into the CSVs. 
* `tgs_analyse_game_csv.py`: a python script to analyse the game level statistics. It will provide stats and graphs corresponding to the viewer trends, average viewership etc.
* `tgs_analyse_channel_csv.py`: a python script to analyse the channel level statistics. It will provide stats and graphs corresponding to things like the top streamers and so forth.
* `tgs_compare_two_games.py`: a python script to compare two game CSVs. Which game will come out top?

THese scripts are intended to be used with `python3`.