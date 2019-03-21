import pickle
import pprint as pp
from bs4 import BeautifulSoup
import requests
import pickle
import os.path
from collections import OrderedDict
from PlattentestsApi import PlattentestsApi
import datetime
from operator import itemgetter

def get_names():
    '''Create filename and playlist name'''
    now = datetime.datetime.now()
    year = str(now.isocalendar()[0])
    week = str(now.isocalendar()[1])
    filename = "week-" + year + "-" + week + ".pickle"
    playlist_name = "Plattentests.de Archiv Highlights der Woche " + year + "-" + week
    return filename, playlist_name

def edit_track(filename, track_n, new_track):
    '''Replace a track of a saved playlist'''
    pickle_off = open(filename, "rb")
    playlist = pickle.load(pickle_off)

    print("old: %s" % playlist[track_n])
    playlist[track_n] = new_track
    print("new: %s" % playlist[track_n])
    print("")

    pickling_on = open(filename,"wb")
    pickle.dump(playlist, pickling_on)
    pickling_on.close()

def add_to_playlist_archive(playlist_id, playlist_filename):
    print("Updating playlist archive:")
    if os.path.exists("playlist_archive.pickle"):
        ## Load playlist archive
        pickle_off = open("playlist_archive.pickle","rb")
        playlist_archive = pickle.load(pickle_off)

        ## Update playlist archive
        playlist_archive[playlist_filename[:-7]] = playlist_id
        pp.pprint(playlist_archive)
        print("")

        ## Save playlist archive
        pickling_on = open("playlist_archive.pickle","wb")
        pickle.dump(playlist_archive, pickling_on)
        pickling_on.close()
    else:
        pickling_on = open("playlist_archive.pickle","wb")
        playlist_archive = {playlist_filename[:-7]: playlist_id}
        pickle.dump(playlist_archive, pickling_on)
        pickling_on.close()


def trailing_space(s):
    if s[-1] == " ":
        return s[:-1]
    else: return s


def update_adw():
    '''
    check for existing album of the week and
    save the initial current adw as .pickle
    return: major Plattentests.de update True or False
    '''
    major_update = False

    print("Looking for adw ...")
    if os.path.exists("adw_current.pickle"):
        print("Exists!")
        filename = "adw_current.pickle"
        pickle_off = open(filename,"rb")
        adw_old = pickle.load(pickle_off)
        adw_new = PlattentestsApi.getAlbumOfTheWeek()

        if adw_old == adw_new:
            print("No new adw. Initiate minor update!")
            print("")
        else:
            pickling_on = open("adw_current.pickle","wb")
            pickle.dump(adw_new, pickling_on)
            pickling_on.close()
            print("New adw found!")
            print("Writing '%s' in adw_current.pickle" % adw_new)
            print("Initiate major update!")
            print("")
            major_update = True

    else:
        print("No current adw.")
        adw = PlattentestsApi.getAlbumOfTheWeek()
        pickling_on = open("adw_current.pickle","wb")
        pickle.dump(adw, pickling_on)
        pickling_on.close()
        print("Writing '%s' in adw_current.pickle" % adw)
        print("Initiate major update!")
        print("")
        major_update = True

    return major_update

def repair_adw():
    '''
    repairs current adw
    '''

    print("Retrieving adw ...")
    adw_new = PlattentestsApi.getAlbumOfTheWeek()
    pickling_on = open("adw_current.pickle","wb")
    pickle.dump(adw_new, pickling_on)
    pickling_on.close()
    print("Writing '%s' in adw_current.pickle" % adw_new)
    print("")


class MyOrderedDict(OrderedDict):
    def last(self):
        k=next(reversed(self))
        return (k,self[k])

def get_weekly_filename_and_ID():
    pickle_off = open("playlist_archive.pickle","rb")
    playlist_archive = pickle.load(pickle_off)
    d = MyOrderedDict(playlist_archive)
    weekly_id = d.last()[1]
    filename = d.last()[0] + ".pickle"
    return filename, weekly_id


def sortTrackHighlights(trackHighlights, scoreValues):
    '''Sort links and artists by review score'''
    listToSort = [[score, trackHighlights[i],] for i, score in enumerate(scoreValues)]
    listToSort2 = sorted(listToSort, key=itemgetter(1))
    sortedList = sorted(listToSort, key=itemgetter(0), reverse=True)
    sortedTracks = []
    for album in sortedList:
        if album[1] != []:
            for track in album[1]:
                sortedTracks.append(track)

    return sortedTracks


