from bs4 import BeautifulSoup
import requests
import pickle
from parser_ import *
from spotify_api import *
from tools import *
import os.path
import pprint as pp


major_update = update_adw()

if major_update == True:
	print("Running major update...")
	## Parse plattentests.de and create playlist
	links = get_releases()
	links2, artists2 = sort_by_score(links)
	playlist = get_playlist(links2, artists2)
	pp.pprint(playlist)

	## Save playlist
	filename, playlist_name = get_names()
	pickling_on = open(filename,"wb")
	pickle.dump(playlist, pickling_on)
	pickling_on.close()
	print("Playlist saved as '%s'." % filename)

	## Search track IDs on Spotify
	track_IDs = (get_IDs(playlist))

	## Create a new playlist on Spotify and add ID to archive
	playlist_id = create_playlist(playlist_name)
	add_to_playlist_archive(playlist_id, filename)

	## Add tracks to new playlist
	add_tracks_to_playlist(playlist_id, track_IDs)

	#Update playlist (master id: '00zZ5RKsSREcklyEy0tVYU')
	update_playlist("00zZ5RKsSREcklyEy0tVYU", track_IDs)

## Minor update: don't parse for new highlight songs,
# just search on spotify and update the playlist for newly released songs
else:
	## Load current playlist
	print("Running minor update...")
	filename, weekly_id = get_weekly_filename_and_ID()
	pickle_off = open(filename,"rb")
	playlist = pickle.load(pickle_off)
	print("Playlist '%s' loaded." % filename)
	print("")

	## Search track IDs on Spotify
	track_IDs = (get_IDs(playlist))

	## Compare old IDs with new IDs
	track_IDs_old = read_playlist("00zZ5RKsSREcklyEy0tVYU", "masilenus")

	if len(track_IDs) >= len(track_IDs_old):
		if track_IDs != track_IDs_old:
			## Update master playlist (master id: '00zZ5RKsSREcklyEy0tVYU')
			update_playlist("00zZ5RKsSREcklyEy0tVYU", track_IDs)

			## Update weekly playlist
			update_playlist(weekly_id, track_IDs)

		else:
			print("Not updated. No corrected tracks found.")

	else:
		print("Not updated. No additional tracks found.")










