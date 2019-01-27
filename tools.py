import pickle
import pprint as pp
from bs4 import BeautifulSoup
import requests
import pickle
import os.path
from collections import OrderedDict
from PlattentestsApi import PlattentestsApi


class MyOrderedDict(OrderedDict):
    def last(self):
        k=next(reversed(self))
        return (k,self[k])

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
    currentAlbumOfTheWeek = PlattentestsApi.getAlbumOfTheWeek()
    if os.path.exists("adw_current.pickle"):
        print("Exists!")
        filename = "adw_current.pickle"
        pickle_off = open(filename,"rb")
        adw_old = pickle.load(pickle_off)

        if adw_old == currentAlbumOfTheWeek:
            print("No new adw. Initiate minor update!")
            print("")
        else:
            pickling_on = open("adw_current.pickle","wb")
            pickle.dump(currentAlbumOfTheWeek, pickling_on)
            pickling_on.close()
            print("New adw found!")
            print("Writing '%s' in adw_current.pickle" % currentAlbumOfTheWeek)
            print("Initiate major update!")
            print("")
            major_update = True

    else:
        print("No current adw.")
        pickling_on = open("adw_current.pickle","wb")
        pickle.dump(currentAlbumOfTheWeek, pickling_on)
        pickling_on.close()
        print("Writing '%s' in adw_current.pickle" % currentAlbumOfTheWeek)
        print("Initiate major update!")
        print("")
        major_update = True

    return major_update

def get_weekly_filename_and_ID():
    pickle_off = open("playlist_archive.pickle","rb")
    playlist_archive = pickle.load(pickle_off)
    d = MyOrderedDict(playlist_archive)
    weekly_id = d.last()[1]
    filename = d.last()[0] + ".pickle"
    return filename, weekly_id

