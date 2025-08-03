import streamlit as st
import pandas as pd
import spotipy
import re
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(page_title="Analyse Spotify Playlist", layout="wide")
st.title("Analyse de votre playlist Spotify")

# Fonction pour extraire l'ID depuis un lien
def extract_playlist_id(link):
    match = re.match(r"https://open.spotify.com/playlist/([a-zA-Z0-9]+)", link)
    return match.group(1) if match else link.strip()

# Authentification
TOKEN_PATH = "spotify_token.json"

try:
    if not os.path.exists(TOKEN_PATH) or os.path.getsize(TOKEN_PATH) == 0:
        raise ValueError("Token manquant ou fichier vide")

    with open(TOKEN_PATH, "r") as f:
        token_info = json.load(f)

    if not (access_token := token_info.get("access_token")):
        raise ValueError("Access token manquant")

    sp = spotipy.Spotify(auth=access_token)

except Exception as e:
    st.error(f"Erreur d'authentification : {e}. Veuillez vous authentifier.")
    st.stop()

# Interface utilisateur
playlist_input = st.text_input("Entrez le lien ou l'ID de votre playlist Spotify :", "")

if playlist_input:
    playlist_id = extract_playlist_id(playlist_input)

    try:
        # Récupération des pistes de la playlist
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']
        
        # Pagination pour les grandes playlists
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        # Extraction des métadonnées de base
        data = []
        for track in tracks:
            if not (info := track.get("track")):
                continue
                
            name = info.get("name")
            primary_artist = info.get("artists", [{}])[0].get("name")
            album = info["album"].get("name")
            release_date = info["album"].get("release_date")
            popularity = info.get("popularity")
            duration_ms = info.get("duration_ms")
            
            # Conversion de la durée
            duration = f"{duration_ms//60000}:{(duration_ms%60000)//1000:02d}" if duration_ms else None
            
            # Genres (via l'artiste principal)
            artist_id = info.get("artists", [{}])[0].get("id")
            genres = []
            if artist_id:
                try:
                    artist_data = sp.artist(artist_id)
                    genres = artist_data.get("genres", [])
                except:
                    pass

            data.append([
                name, 
                primary_artist, 
                album, 
                release_date, 
                popularity, 
                duration,
                ", ".join(genres[:3])  # Limite à 3 genres
            ])

        # Création du DataFrame
        df = pd.DataFrame(data, columns=[
            "Titre", "Artiste", "Album", 
            "Date de sortie", "Popularité", 
            "Durée", "Genres"
        ])

        if df.empty:
            st.warning("Aucun titre trouvé dans cette playlist.")
            st.stop()

        st.success(f"{len(df)} titres trouvés dans la playlist.")
        
        # Affichage des données brutes avec option de téléchargement
        st.subheader("Liste des titres")
        st.dataframe(df)
        
        if st.button("Télécharger les données"):
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Télécharger en CSV",
                data=csv,
                file_name="playlist_spotify.csv",
                mime="text/csv"
            )

        # Analyses de base
        st.subheader("Statistiques de base")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nombre de titres", len(df))
            st.metric("Artistes uniques", df['Artiste'].nunique())
        
        with col2:
            st.metric("Album le plus fréquent", df['Album'].mode()[0] if not df['Album'].empty else "N/A")
            
            # Calcul plus robuste de l'année moyenne
            try:
                df['Année'] = pd.to_datetime(df['Date de sortie'], errors='coerce').dt.year
                avg_year = df['Année'].mean()
                st.metric("Année moyenne", int(avg_year) if not pd.isna(avg_year) else "N/A")
            except:
                st.metric("Année moyenne", "N/A")
        
        with col3:
            st.metric("Popularité moyenne", round(df['Popularité'].mean(), 1))
            st.metric("Durée la plus fréquente", df['Durée'].value_counts().index[0] if not df['Durée'].empty else "N/A")

        # Visualisations
        st.subheader("Analyse des données")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "Popularité", "Artistes", "Genres", "Années"
        ])
        
        with tab1:
            st.subheader("Top 50 par popularité")
            top50 = df.nlargest(50, 'Popularité')
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(data=top50, x='Titre', y='Popularité', ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            ax.set_title("Top 50 des titres les plus populaires")
            st.pyplot(fig)
            
            st.subheader("Distribution de la popularité")
            fig2, ax2 = plt.subplots()
            sns.histplot(df['Popularité'], bins=20, kde=True, ax=ax2)
            ax2.set_title("Distribution des scores de popularité")
            st.pyplot(fig2)
        
        with tab2:
            st.subheader("Top 10 artistes")
            top_artists = df['Artiste'].value_counts().head(10)
            st.bar_chart(top_artists)
            
            st.subheader("Top 10 artistes (popularité moyenne)")
            artist_stats = df.groupby('Artiste')['Popularité'].agg(['mean', 'count'])
            top_artists_pop = artist_stats[artist_stats['count'] >= 3].nlargest(10, 'mean')
            st.bar_chart(top_artists_pop['mean'])
        
        with tab3:
            if not df['Genres'].empty:
                st.subheader("Genres les plus fréquents")
                genres_exp = df['Genres'].str.split(', ').explode()
                top_genres = genres_exp.value_counts().head(10)
                st.bar_chart(top_genres)
                
                st.subheader("Nuage de mots des genres")
                text = ' '.join(genre for genre in genres_exp if genre != '')
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
                st.image(wordcloud.to_array())
            else:
                st.warning("Aucune donnée de genre disponible")
        
        with tab4:
            if 'Année' in df.columns:
                st.subheader("Répartition par année")
                year_counts = df['Année'].value_counts().sort_index()
                st.bar_chart(year_counts)
                
                st.subheader("Évolution de la popularité")
                year_pop = df.groupby('Année')['Popularité'].mean()
                st.line_chart(year_pop)
            else:
                st.warning("Données d'année non disponibles")

    except Exception as e:
        st.error(f"Erreur lors de la récupération de la playlist : {str(e)}")
