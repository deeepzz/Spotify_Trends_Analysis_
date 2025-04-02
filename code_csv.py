"""Get song titles and artists from Spotify playlist"""

import csv
import os
import re

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# load credentials from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
OUTPUT_FILE_NAME = "track_info.csv"

# change for your target playlist
PLAYLIST_LINK = "https://open.spotify.com/playlist/739m9cmQb44KK7PvF9H2ws?si=af8e9a065c374f5f"

# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# get uri from https link
if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
    playlist_uri = match.groups()[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")

# get list of tracks in a given playlist (note: max playlist length 100)
tracks = session.playlist_tracks(playlist_uri)["items"]

# create csv file
with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # write header column names
    writer.writerow(["track", "artist", "album","popularity", "track id"])

    # extract name and artist
    for track in tracks:
        track_info = track["track"]
        if not track_info:
            continue
        name = track["track"]["name"]
        artists = ", ".join(
            [artist["name"] for artist in track["track"]["artists"]]
        )
        album = track_info["album"]["name"]
        popularity = track_info.get("popularity", "")
        track_id = track_info.get("id", "")

        # write to csv
        writer.writerow([name, artists, album, popularity,track_id])
