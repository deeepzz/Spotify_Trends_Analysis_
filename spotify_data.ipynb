import os
import random
import string
import urllib.parse
import pandas as pd
import streamlit as st
from flask import Flask, redirect, request
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "playlist-read-private"

# Flask App for OAuth
app = Flask(__name__)

# Generate random state string
def generate_state(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/login")
def login():
    state = generate_state()
    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": SPOTIPY_CLIENT_ID,
        "scope": SCOPE,
        "redirect_uri": SPOTIPY_REDIRECT_URI,
        "state": state
    })
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    auth_manager = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    )
    token_info = auth_manager.get_access_token(code, as_dict=True)
    global sp
    sp = spotipy.Spotify(auth=token_info["access_token"])
    return "Authentication successful. You may now close this tab."

# Default fallback if OAuth was not used
auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=SCOPE)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_playlist_artists(playlist_id):
    try:
        results = sp.playlist_tracks(playlist_id)
        if not results or "items" not in results or not results["items"]:
            st.error("No tracks found! Playlist may be empty, private, or unavailable.")
            return pd.DataFrame()

        artist_data = {}
        for item in results["items"]:
            track = item.get("track")
            if track and "artists" in track:
                for artist in track["artists"]:
                    artist_id = artist["id"]
                    if artist_id not in artist_data:
                        artist_info = sp.artist(artist_id)
                        artist_data[artist_id] = {
                            "name": artist_info.get("name", "Unknown"),
                            "genres": ', '.join(artist_info.get("genres", [])),
                            "popularity": artist_info.get("popularity", 0),
                            "followers": artist_info.get("followers", {}).get("total", 0)
                        }
        return pd.DataFrame(artist_data.values())
    except spotipy.exceptions.SpotifyException as e:
        st.error(f"Spotify API Error ({e.http_status}): {e.msg}")
        return pd.DataFrame()

def main():
    st.title("Spotify Playlist Artists Analysis 🎵")

    playlist_id = st.text_input("Enter Spotify Playlist ID", "")

    if playlist_id:
        df_artists = get_playlist_artists(playlist_id)

        if df_artists.empty:
            st.warning("No artist data found! Check if the playlist is available.")
            return

        st.write("### Artists in Playlist")
        st.dataframe(df_artists)

        st.write("### Artist Popularity Distribution")
        st.bar_chart(df_artists.set_index("name")["popularity"])

        st.write("### Most Popular Artists")
        top_artists = df_artists.sort_values(by="popularity", ascending=False).head(10)
        st.dataframe(top_artists)

        st.write("### Most Followed Artists")
        most_followed = df_artists.sort_values(by="followers", ascending=False).head(10)
        st.dataframe(most_followed)

if __name__ == "__main__":
    main()

