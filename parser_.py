from bs4 import BeautifulSoup
import requests
import pickle
import pprint
import datetime
from collections import OrderedDict


def get_releases():
    '''
    Get the lists of links to single reviews (rezis)
    '''
    print("Retrieving new reviews from plattentests.de ...")     
    r = requests.get("https://www.plattentests.de/")
    soup = BeautifulSoup(r.text, "html.parser")
    rezis_box = soup.find("div", attrs={"class":"box neuerezis"})

    links = []

    for a in rezis_box.find_all('a', href=True):
        links.append("https://www.plattentests.de/" + a['href'])
        
    return links


def get_score(url):
    '''Get review score for a single review'''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    rezi_box = soup.find("div", attrs={"class":"headerbox rezi"})
    rezi_text = rezi_box.find_all('h1')[0].text
    artist = rezi_text.split("-")[0]
    artist = artist[:-1]
    if get_adw() == get_album_title(url):
        return artist, 11  # adw get artificial score of 11 to improve sorting
    else:
        bewertung = soup.find("p", attrs={"class":"bewertung"})
        score = bewertung.find_all('strong')[0].text.split("/")[0]
        if score == "Ohne Bewertung":
            score = 0
        return artist, int(score)


def sort_by_score(links):
    '''Sort links and artists by review score'''
    print("Collecting ratings ...")
    artists = []
    scores = []
    for link in links:
        artist, score = get_score(link)
        artists.append(artist)
        scores.append(score)

    link_lst = [[scores[i], link, artists[i],] for i, link in enumerate(links)]
    link_lst_sorted = sorted(link_lst, reverse=True)
    artists2 = [element[2] for element in link_lst_sorted]
    links2 = [element[1] for element in link_lst_sorted]

    return links2, artists2


def get_highlights(url, artist):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    rezis_box = soup.find("div", attrs={"id":"rezihighlights"})
    
    highlights = []
    
    for li in rezis_box.find_all('li'):
        if li.text != "-":
            highlights.append(artist + " - " + li.text)
        else:
            print("%s has no highlights" % artist)
        
    if highlights != []:
        return highlights


def get_playlist(links, artists):
    '''Look-up Highlight tracks for each review'''

    print("Collecting highlight tracks ...")

    def clean_playlist(playlist):
        '''Clean-up track and artist names for better search'''
        playlist_new = []
        for song in playlist:
            t = song.replace("&amp;", "&")
            playlist_new.append(t)    
        return playlist_new

    playlist = []
    for i, link in enumerate(links):
        highlights = get_highlights(link, artists[i])

        if highlights is not None:
            for song in highlights:
                playlist.append(song)
        
    return clean_playlist(playlist)


def get_names():
    '''Create filename and playlist name'''
    now = datetime.datetime.now()
    year = str(now.isocalendar()[0])
    week = str(now.isocalendar()[1])
    filename = "week-" + year + "-" + week + ".pickle"
    playlist_name = "Plattentests.de Archiv Highlights der Woche " + year + "-" + week
    return filename, playlist_name


## For future features:
def get_adw():
    '''Return album of the week'''
    r = requests.get("https://www.plattentests.de/index.php")
    soup = BeautifulSoup(r.text, "html.parser")
    adw_box = soup.find("div", attrs={"class":"headerbox adw"})
    adw_text = adw_box.find_all('h3')[0].text
    return adw_text


def get_album_title(url):
    '''Returns album title of review'''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    rezi_box = soup.find("div", attrs={"class":"headerbox rezi"})
    rezi_text = rezi_box.find_all('h1')[0].text
    return rezi_text

