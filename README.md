Spotify Playlist Analyzer – Projet Data & IA

Depuis novembre 2024, Spotify a restreint l'accès à plusieurs endpoints de son API, notamment ceux liés aux audio features.
Malgré ces limitations, j'ai réussi à réaliser une analyse musicale complète à partir des données encore disponibles.
Aujourd'hui, je vous présente la partie interactive de ce projet, qui permet d'explorer ses playlists directement depuis une application Streamlit.

Fonctionnalités
- Authentification sécurisée à l'API Spotify
- Extraction automatique des métadonnées d’une playlist
- Visualisation de statistiques clés (artistes, genres, années, popularité)
- Analyse comparative entre deux playlists (anglophone vs tamoule)
- Visualisations interactives via Streamlit et Power BI
- Structuration des données dans une base SQL et analyses avancées

Étape 1 – Authentification Spotify avec Flask et Streamlit
- Authentification OAuth 2.0 avec récupération automatique du token via Flask
- Stockage du token dans spotify_token.json pour éviter la reconnexion
- Vérification et rafraîchissement automatique du token en cas d’expiration
Bibliothèques utilisées : json, requests, streamlit, datetime

Étape 2 – Extraction des données via l’ID de la playlist
- Champ de saisie dans l'application Streamlit pour entrer l'ID ou le lien de la playlist
- Extraction de l’ID via expressions régulières
- Appel à l’API Spotify pour récupérer les morceaux
Bibliothèques utilisées : spotipy, re, streamlit

Étape 3 – Visualisation dans Streamlit
- Affichage des playlists avec st.dataframe() et st.bar_chart()
- Statistiques générées avec seaborn :  "Top 50 morceaux populaires" ; "Top 10 artistes" ; "Titres les plus récurrents" ; "Répartition des genres" ; "Répartition par année de sortie"
Bibliothèques utilisées : pandas, seaborn

Analyse comparative : playlists anglophones vs tamoules
Deux playlists ont été comparées :
Une playlist anglophone
Une playlist tamoule

Traitement complémentaire:
- Extraction et sauvegarde CSV
- Authentification via Flask
- Extraction des métadonnées de chaque piste (titre, artiste, popularité, etc.)
- Sauvegarde dans un fichier track_info.csv
Bibliothèques utilisées : flask, json, requests, spotipy, dotenv, os, re, csv

Nettoyage des données:
- Chargement du fichier CSV avec pandas
- Analyse des dimensions (shape), valeurs manquantes (isnull()), types de données (info()), statistiques descriptives (describe())
Bibliothèques utilisées : numpy, pandas

Exploration des données : 
- Analyse des artistes, albums et morceaux les plus populaires (value_counts)
- Statistiques sur la popularité (moyenne, max, min)
- Croisements artistes / albums / popularité
Bibliothèques utilisées : matplotlib, seaborn

Structuration SQL et reporting
- Création d’une table SQL avec les colonnes : track, album, release_date, artist, popularity, genre
- Types de colonnes utilisés : VARCHAR, FLOAT, BOOLEAN, INT

Nettoyage : suppression des chansons à durée nulle, normalisation des données
- Exemples de requêtes : "Lister les 10 morceaux les plus populaires" ; "Répartition des morceaux par année" ; "Répartition des genres dominants" ; "Visualisations finales réalisées sous Power BI"
Bibliothèques utilisées : SQL, SQLite, Power BI

Résultats clés
-
- Une majorité de titres provient des dix dernières années
- Les artistes tamouls sont souvent associés à une diversité de genres, contrairement aux artistes anglophones plus récents
Ce constat illustre une évolution de l’industrie musicale : autrefois centrée sur le genre, elle est aujourd’hui influencée par l’ambiance ou l’émotion des morceaux, renforcée par les algorithmes de streaming
- Plus de 70 % des morceaux analysés ont une popularité supérieure à 60
- Certains genres très présents dans les playlists ne correspondaient pas à ceux que je pensais écouter le plus, montrant l'intérêt d'une analyse objective des données

Et vous ?
Que souhaiteriez-vous apprendre sur vos propres playlists ?
Êtes-vous plutôt orienté musique grand public ou explorateur de morceaux rares ?

