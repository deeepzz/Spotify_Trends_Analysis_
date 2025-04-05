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

# Configuration de la page
st.set_page_config(page_title="Analyse Spotify", layout="wide")

# Titre
st.title("Analyse interactive de playlists Spotify")

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

# Champ de saisie utilisateur
playlist_input = st.text_input("Entrez le lien ou l’ID d’une playlist Spotify :", "")

if playlist_input:
    playlist_id = extract_playlist_id(playlist_input)

    try:
        # Récupération des pistes
        results = sp.playlist_tracks(playlist_id)
        tracks = results["items"]
        data = []
        for track in tracks:
            info = track["track"]
            if info:
                name = info["name"]
                artists_info = info["artists"]
                artists = ", ".join([artist["name"] for artist in artists_info])
                album = info["album"]["name"]
                track_id = info.get("id", "")
                release_date = info["album"].get("release_date", None)
                popularity = info.get("popularity", None)

            data.append([name, artists, album, release_date, popularity, track_id])
        df = pd.DataFrame(data, columns=["track", "artist", "album", "release_data", "popularity", "track_id"])

        if df.empty:
            st.warning("Aucun titre trouvé dans cette playlist.")
        else:
            st.success(f"{len(df)} titres extraits depuis la playlist.")
            st.dataframe(df)

            # Popularité par morceau
            st.subheader("Popularité des morceaux (Top 30)")
            df_sorted = df.sort_values(by="popularity", ascending=False).head(30)
            fig1, ax = plt.subplots(figsize=(14, 6))
            sns.barplot(data=df_sorted, x="track", y="popularity", ax=ax)
            ax.set_title("Popularité des morceaux", fontsize=16, weight='bold')
            ax.set_xlabel("Titre", fontsize=12)
            ax.set_ylabel("Popularité", fontsize=12)
            plt.xticks(rotation=90)
            st.pyplot(fig1)

            # Top artistes
            st.subheader("Top 5 artistes les plus présents")
            top_artists = df["artist"].value_counts().head(5)
            st.bar_chart(top_artists)

            # Titres les plus populaires
            st.subheader("Titres les plus populaires")
            top_tracks = df.sort_values(by="popularity", ascending=False).head(5)
            st.table(top_tracks[["track", "artist", "popularity"]])

            # Nuage de mots
            if st.checkbox("Afficher le nuage de mots des titres"):
                text = " ".join(df["track"].dropna())
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
                fig2, ax = plt.subplots(figsize=(10, 4))
                ax.imshow(wordcloud, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig2)

    except Exception as e:
        st.error(f"Erreur lors de la récupération de la playlist : {e}")
