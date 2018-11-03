import pickle
import pprint as pp
from bs4 import BeautifulSoup
import requests
import pickle
from parser_ import get_adw
import os.path
from collections import OrderedDict


class MyOrderedDict(OrderedDict):
    def last(self):
        k=next(reversed(self))
        return (k,self[k])


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
        adw_new = get_adw()

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
        adw = get_adw()
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
    adw_new = get_adw()
    pickling_on = open("adw_current.pickle","wb")
    pickle.dump(adw_new, pickling_on)
    pickling_on.close()
    print("Writing '%s' in adw_current.pickle" % adw_new)
    print("")


def get_weekly_filename_and_ID():
    pickle_off = open("playlist_archive.pickle","rb")
    playlist_archive = pickle.load(pickle_off)
    d = MyOrderedDict(playlist_archive)
    weekly_id = d.last()[1]
    filename = d.last()[0] + ".pickle"
    return filename, weekly_id

