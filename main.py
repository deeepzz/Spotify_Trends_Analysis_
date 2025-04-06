import streamlit as st
import pandas as pd
import spotipy
from dotenv import load_dotenv
import os
import re
import json
import requests
import statistics
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from spotipy.oauth2 import SpotifyClientCredentials

st.set_page_config(page_title="Analyse spotify playlist", layout="wide")
st.title("Analyse de votre playlist spotify ;) ")

# Fonction pour extraire l'ID depuis un lien
def extract_playlist_id(link):
    match = re.match(r"https://open.spotify.com/playlist/([a-zA-Z0-9]+)", link)
    return match.group(1) if match else link.strip()

# Champ de saisie utilisateur
playlist_input = st.text_input("Entrez le lien ou l’ID de votre playlist Spotify :", "")

# Authentification Spotipy via token sauvegardé par Flask
try:
    with open("spotify_token.json", "r") as f:
        token_info = json.load(f)
        access_token = token_info.get("access_token")
        expires_at = token_info.get("expires_at")

        if not access_token:
            raise ValueError("access_token manquant")

        now = datetime.now().timestamp()
        if expires_at and now > expires_at:
            st.warning("Token expiré, tentative de rafraîchissement...")
            refresh_url = "https://curly-cod-4xw6rvj9wpxc7q44-8502.app.github.dev/refresh-token"
            refresh_response = requests.get(refresh_url)
            if refresh_response.status_code == 200:
                with open("spotify_token.json", "r") as f:
                    token_info = json.load(f)
                    access_token = token_info.get("access_token")
                    if not access_token:
                        raise ValueError("Token toujours manquant après rafraîchissement.")
                    st.success("Token rafraîchi !")
            else:
                st.error("Échec du rafraîchissement automatique du token.")
                st.stop()

        sp = spotipy.Spotify(auth=access_token)

except Exception as e:
    st.error(f"Token invalide : {e}. Va sur `/login` pour t’authentifier.")
    st.stop()

if playlist_input:
    playlist_id = extract_playlist_id(playlist_input)

    try:
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        data = []
        for track in tracks:
            info = track.get("track")
            if info:
                name = info.get("name")
                primary_artist = info.get("artists", [{}])[0].get("name")
                album = info["album"].get("name")
                track_id = info.get("id")
                release_date = info["album"].get("release_date")
                popularity = info.get("popularity")

                # Get primary artist ID and fetch genres
                artist_id = info.get("artists", [{}])[0].get("id")
                genres = []
                if artist_id:
                    try:
                        artist_data = sp.artist(artist_id)
                        genres = artist_data.get("genres", [])
                    except:
                        genres = []

                data.append([name, primary_artist, album, release_date, popularity, track_id, ", ".join(genres)])

        df = pd.DataFrame(data, columns=["track", "artist", "album", "release_data", "popularity", "track_id", "genres"])

        load_dotenv()
        CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
        CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
        client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

        if df.empty:
            st.warning("Aucun titre trouvé dans cette playlist.")
        else:
            st.success(f"{len(df)} titres extraits depuis la playlist.")

            st.dataframe(df)

            st.subheader("Top 50 : ")
            df_sorted = df.sort_values(by="popularity", ascending=False).head(50)
            fig1, ax = plt.subplots(figsize=(14, 6))
            sns.barplot(data=df_sorted, x="track", y="popularity", ax=ax)
            ax.set_title("Popularité des morceaux", fontsize=16, weight='bold')
            ax.set_xlabel("Titre", fontsize=12)
            ax.set_ylabel("Popularité", fontsize=12)
            plt.xticks(rotation=90)
            st.pyplot(fig1)

            st.subheader("Top 10 artistes")
            top_artists = df["artist"].value_counts().head(10)
            st.bar_chart(top_artists)

            st.subheader("Tes 10 chansons préférées")
            top_tracks = df.sort_values(by="popularity", ascending=False).head(10)
            st.table(top_tracks[["track", "artist", "popularity"]])

            st.subheader("Genres les plus fréquents")
            genre_counts = df["genres"].str.split(", ").explode().value_counts().head(10)
            st.bar_chart(genre_counts)

            st.subheader("Répartition des morceaux par année de sortie")
            df["release_year"] = pd.to_datetime(df["release_data"], errors='coerce').dt.year
            year_counts = df["release_year"].value_counts().sort_index()
            fig_years, ax_years = plt.subplots(figsize=(10, 4))
            sns.barplot(x=year_counts.index.astype(str), y=year_counts.values, ax=ax_years)
            ax_years.set_title("Nombre de morceaux par année", fontsize=14)
            ax_years.set_xlabel("Année")
            ax_years.set_ylabel("Nombre de morceaux")
            plt.xticks(rotation=45)
            st.pyplot(fig_years)

    except Exception as e:
        st.error(f"Erreur lors de la récupération de la playlist : {e}")
