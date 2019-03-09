# Plattentests-Spotipy

A python program to automatically collect recent highlight songs of Plattentests.de music reviews. Interactions with the Spotify Web API are based on plamere's Spotipy: https://github.com/plamere/spotipy



## Dependencies

In addition to Python 3.6, plattentests-spotipy needs the following python libraries installed:

- Spotipy -> `pip install spotipy`
- Beautifulsoup4 -> `pip install beautifulsoup4`
- Termcolor -> `pip install termcolor`

Furthermore, these standard python libraries are being used: **requests, pickle, os.path, pprint, datetime, json, collections.**



## Usage

### Getting started

1. Register the Spotify Web App at https://developer.spotify.com/documentation/web-api/.
   
2. Duplicate `constants.py.example` and rename it to `constants.py`
   
3. Add the Spotify credentials to the `constants.py` file. Those include: **username, client_id,** and **client_secret**. Spotify will provide client_id and client_secret after registering the app. Also, add a **redirect_uri**, e.g. http://localhost:8888/callback/.
   
4. Create a playlist on Spotify and save its ID which is the cryptic combination of letters and numbers at the end of the Spotify URI (right click on playlist in the Spotify Desktop App -> Share -> Copy Spotify URI). Use this ID as "master" playlist ID and add it to the `constants.py` file. The master playlist will be constantly updated. Additionally, an "archive" playlist is created weekly.
   
5. Execute  `run-everytime-update.py`. When running the app for the first time, the Spotify API will ask you to login. Please see https://github.com/plamere/spotipy for more details.
   
6. Please note that two .pickle files will be created in your folder:

   `adw_current.pickle` stores the current album of the week

   `week_YEAR_WEEK.pickle` archives the highlight songs fetched from plattentests.de

### Common use cases

#### Update master playlist

Execute `run-everytime-update.py`. The program will automatically update the master playlist if there are new reviews on plattentests.de or if there are any new releases on Spotify.

#### Edit single songs of the playlist

Sometimes artist or title of a song don't match between plattentests.de and Spotify. There will be warnings printed in the terminal, when this happens. One can edit the mismatched song using the `edit_track()` function. Place this function in some .py file and run it.

`edit_track(filename, track_n, new_track)`

filename (str): .pickle file containing the archived highlight songs

track_n (int): number associated with the song; is printed in the terminal log following the asterisk*

new_track (str): user-defined edit of song; use format "Artist - Title".

## Authors

- tmdecker

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.