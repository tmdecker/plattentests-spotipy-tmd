from datetime import datetime

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from termcolor import colored

import constants
from tools import trailing_space


def get_IDs(playlist):
    print("Searching spotify for tracks ...")

    client_credentials_manager = SpotifyClientCredentials(client_id=constants.client_id,
                                                          client_secret=constants.client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    IDs = []
    for i, track in enumerate(playlist):
        print(track + "* " + str(i))

        # Titles are truncated after brackets because this is a major
        # source of title mismatch during Spotify search.
        # Brackets at beginning of title are not truncated.
        if track.split(" - ")[1][1] == ("("):
            q = track.split("(")[0]+"("+track.split("(")[1]
        else:
            q = track.split("(")[0]

        results = sp.search(q=q, limit=7)

        if len(results['tracks']['items']) == 0:
            print(colored("Song not found.", "red"))

        for t in results['tracks']['items']:
            artists = [artist["name"].lower() for artist in t["artists"]]

            # Check 3: Release year in the present? Important for live LPs or Best Ofs
            if date_check(t) == True:
                # Check 1: matching artists
                if trailing_space(track.split(" - ")[0].lower()) in artists:  

                    sp_title = t["name"].split(" - ")[0].lower()
                    pt_title = track.split(" - ")[1].lower()

                    # Check 2: matching title
                    # Potentially error-prone if same track exists as solo AND collaboration:
                    # In this case feat. artists are ignored and might return the wrong version
                    # However, Date-Check might correct for this behaviour in many cases.   
                    if sp_title in pt_title:  
                        if len(artists) == 1:
                            print("%s - %s" % (artists[0], t["name"],))
                        else:
                            print("%s - %s (feat. %s)" % (artists[0], t["name"], artists[1],))
                    
                        IDs.append(t["id"])
                        break

                    else:
                        print(colored("Title missmatch: '%s'" % sp_title, "yellow"))

                else:
                    print(colored("Artist missmatch: '%s'" % artists, "yellow"))
                    continue
            else:  # Check 3 Date check
                continue


    print("%d track IDs of %d found" % (len(IDs), len(playlist)))
    print("")
    return IDs


def create_playlist(playlist_name):
    '''Creates a new playlist for a user'''
    username = constants.username
    scope = 'user-follow-modify playlist-modify'
    client_id = constants.client_id
    client_secret = constants.client_secret
    redirect_uri = constants.redirect_uri

    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri=redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlists = sp.user_playlist_create(username, playlist_name)

    else:
        print("Can't get token for", username)
        
    playlist_id = playlists["id"]
    print("")
    return playlist_id


def add_tracks_to_playlist(playlist_id, track_ids):
    '''Add tracks to spotify playlist'''

    print("Adding tracks to playlist %s on spotify." % playlist_id)

    username = constants.username #placeholder value here
    scope = 'user-follow-modify playlist-modify'
    client_id = constants.client_id #placeholder value here
    client_secret = constants.client_secret #placeholder value here
    redirect_uri = constants.redirect_uri

    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri=redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        print(results)
    else:
        print("Can't get token for", username)
    print("")


def update_playlist(playlist_id, track_ids):
    '''replace all tracks of a spotify playlist'''

    print("Updating playlist %s on spotify." % playlist_id)

    username = constants.username #placeholder value here
    scope = constants.scope
    client_id = constants.client_id #placeholder value here
    client_secret = constants.client_secret #placeholder value here
    redirect_uri = constants.redirect_uri

    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri=redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_replace_tracks(username, playlist_id, track_ids)  # update existing playlist
        print(results)
    else:
        print("Can't get token for", username)
    print("")


def date_check(track):
    release_raw = track["album"]["release_date"]
    release = datetime.strptime(release_raw.split("-")[0], "%Y")
    now = datetime.now()

    # Check if track was released in current year.
    # May be modified for January reviews.
    if release.year == now.year:
        return True

    else: 
        print(colored("Check 3 - old release %d" % release.year, "yellow"))
        return False


def read_playlist(playlist_id, username):
    """returns track_ids of a spotify playlist as list"""

    client_credentials_manager = SpotifyClientCredentials(client_id=constants.client_id,
                                                          client_secret=constants.client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results = sp.user_playlist(username, playlist_id)
    ids = [item["track"]["id"] for item in results["tracks"]["items"]]
    print(f"{len(ids)} IDs found in '{results['name']}'")

    return(ids)
