import pickle
import datetime

def get_names():
    '''Create filename and playlist name'''
    now = datetime.datetime.now()
    year = str(now.isocalendar()[0])
    week = str(now.isocalendar()[1])
    filename = "week-" + year + "-" + week + ".pickle"
    playlist_name = "Plattentests.de Archiv Highlights der Woche " + year + "-" + week
    return filename, playlist_name