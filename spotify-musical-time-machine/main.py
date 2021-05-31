import requests
import datetime as dt

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup


CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://example.com"
STATE = "user-modify-playback-state"
SCOPE = "playlist-modify-private"


date = ""

is_valid = False
while not is_valid:
    date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
    try:
        dt.datetime.strptime(date, "%Y-%m-%d")
        is_valid = True
    except ValueError as e:
        print(f"Incorrect date format. Valid format YYYY-MM-DD - {e}")

# test date
# date = "2000-08-12"

query_resp = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
query_resp.raise_for_status()

soup = BeautifulSoup(query_resp.text, "html.parser")

songs = soup.find_all("span", {"class": "chart-element__information__song"})
artists = soup.find_all("span", {"class": "chart-element__information__artist"})

songs = [song.get_text() for song in songs]
artists = [artist.get_text() for artist in artists]

date_top_100 = list(zip(artists, songs))

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        CLIENT_ID,
        CLIENT_SECRET,
        REDIRECT_URI,
        STATE, SCOPE,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = spotify.current_user()["id"]

search_results = []
for artist, song in date_top_100:
    search_results.append(spotify.search(q=f"artist: {artist} track: {song}", type="track", limit=1))

for idx, result in enumerate(search_results):
    try:
        search_results[idx] = result["tracks"]["items"][0]["uri"]
    except IndexError as e:
        search_results[idx] = ""

search_results = list(filter(None, search_results))

playlist = spotify.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
spotify.playlist_add_items(playlist["id"], items=search_results)
