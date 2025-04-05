import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from spotipy.oauth2 import SpotifyOAuth

# Configuration de la page
st.set_page_config(page_title="Analyse spotify playlist", layout="wide")

# Titre
st.title("Analyse de votre playlist spotify ;) ")

# Chargement des identifiants API
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Authentification Spotipy
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Fonction pour extraire l'ID depuis un lien complet
def extract_playlist_id(link):
    match = re.match(r"https://open.spotify.com/playlist/([a-zA-Z0-9]+)", link)
    if match:
        return match.group(1)
    else:
        return link.strip()

playlist_input = st.text_input("Entrez le lien ou l’ID de votre playlist Spotify :", "")

if playlist_input:
    playlist_id = extract_playlist_id(playlist_input)

    try:
        results = sp.playlist_tracks(playlist_id)
        tracks = results.get("items", [])[:50]  # limite à 50 morceaux

        data = []
        track_ids = []

        for track in tracks:
            info = track.get("track", {})
            if not info:
                continue

            name = info.get("name", "Inconnu")
            artists_info = info.get("artists", [])
            artists = ", ".join([a["name"] for a in artists_info])
            album = info.get("album", {}).get("name", "Inconnu")
            release_date = info.get("album", {}).get("release_date", None)
            popularity = info.get("popularity", None)
            track_id = info.get("id", None)

            track_ids.append(track_id)
            data.append([name, artists, album, release_date, popularity, track_id])

        # Appel groupé pour récupérer les audio features
        audio_features = sp.audio_features(track_ids)
        audio_dict = {feat["id"]: feat for feat in audio_features if feat}

        final_data = []
        for row in data:
            track_id = row[5]
            features = audio_dict.get(track_id, {})
            tempo = features.get("tempo")
            danceability = features.get("danceability")
            final_data.append(row + [tempo, danceability])

        # DataFrame final
        df = pd.DataFrame(final_data, columns=[
            "track", "artist", "album", "release_date", "popularity", "track_id",
            "tempo", "danceability"
        ])
        
        if df.empty:
            st.warning("Aucun titre trouvé dans cette playlist.")
        else:
            st.success(f"{len(df)} titres extraits depuis la playlist.")
            st.dataframe(df)


            # Popularité par morceau
            st.subheader("Top 50 : ")
            df_sorted = df.sort_values(by="popularity", ascending=False).head(50)
            fig1, ax = plt.subplots(figsize=(14, 6))
            sns.barplot(data=df_sorted, x="track", y="popularity", ax=ax)
            ax.set_title("Popularité des morceaux", fontsize=16, weight='bold')
            ax.set_xlabel("Titre", fontsize=12)
            ax.set_ylabel("Popularité", fontsize=12)
            plt.xticks(rotation=90)
            st.pyplot(fig1)

            # Top artistes
            st.subheader("Top 10 artistes")
            top_artists = df["artist"].value_counts().head(10)
            st.bar_chart(top_artists)

            # Titres les plus populaires
            st.subheader("Tes 10 chansons préférés")
            top_tracks = df.sort_values(by="popularity", ascending=False).head(10)
            st.table(top_tracks[["track", "artist", "popularity"]])


    except Exception as e:
        st.error(f"Erreur lors de la récupération de la playlist : {e}")
