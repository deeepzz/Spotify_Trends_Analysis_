Depuis le novembre 2024, Spotify a restreint l'accès à certains endpoints de son API, dont les audio features. Malgré cela, j'ai réussi à réaliser une analyse simple avec les données disponibles et aujourd'hui, je vous présente la partie interactive de mon projet !

Étape 1 – Authentification Spotify avec Streamlit et Flask :

- Récupération du token d’accès via OAuth 2.0 (via Flask). Le token est stocké dans un fichier spotify_token.json pour éviter les reconnexions.
- Vérification du token : token expiré ? un processus de rafraîchissement automatique est mis en place pour garantir un accès continu
- token valide ? effectue les requêtes API
outils : json | requests | streamlit | datetime

Étape 2 – Extraction des données via l'ID de la playlist :

- Champ de saisie : l'utilisateur entre l'ID ou le lien de la playlist via "st.text_input"
- Extraction de l’ID : Extraction de l'ID à partir du lien fourni
- Requête à l’API Spotify : Requête pour récupérer les morceaux de la playlist
Outils : spotipy | re | streamlit

Étape 3 – Visualisation des données dans Streamlit :

- Affichage des données via "st.dataframe()" et "st.bar_chart"
- Statistiques générales via seaborn : "Top 50 titres populaire" ; "Top 10 artists" ; "Top 10 chasons préférés" ; "Genre des artists"; "Répartition par année"
Outils : pandas | seaborn 

Pour rendre les choses plus intéressantes, j'ai décidé de comparer deux playlists : 1 contant des chansons anglophones et 1 avec des chansons tamil! 

Quelques observations intéressantes :
- j'écoute beaucoup de chansons sorties au cours des 10 dernières années.
- Les artistes tamouls sont généralement plus catégorisés dans divers genres musicaux que les nouveaux artistes anglophones ! Effectivement, autrefois, la catégorisation par genre était essentielle pour se faire connaître dans l'industrie musicale (festivales, disco). Aujourd'hui, avec le streaming et les algorithmes, c'est l'ambiance ou l'émotion du morceau qui prime sur le genre. 

Voici la suite du projet Spotify playlist analyzer !



Étape 1 – Extraction des données via l’API Spotify :



-->Authentification sécurisée via flask

-->Récupération de l’URI de la playlist avec re (expressions régulières)

-->Extraction automatique des métadonnées de chaque piste

-->Sauvegarde des données dans un fichier CSV



Bibliothèques utilisées : flask | json |request| spotipy | dotenv | os | re | csv



Étape 2 – Chargement et nettoyage des données (data cleaning):



-->Chargement du fichier track_info.csv dans un DataFrame

-->Vérification du nombre de lignes et colonnes "shape"

-->Identification des valeurs manquantes "isnull().sum()"

-->Inspection des types de données "info()"

-->Analyse statistique de base "describe()"



Bibliothèques utilisées : Numpy | Pandas



Étape 3 – Exploration des données (Data Storytelling):



-->Top artistes, albums et morceaux les plus populaires "value_counts()"

--> Statistiques descriptives : moyenne, max, min sur la popularité

-->Croisement entre popularité, artistes, albums



Bibliothèques utilisées : matplotlib | seaborn



Étape 4 – Modélisation de la base SQL :



-->Création d’une table spotify avec des colonnes pertinentes : track, album, release date, artist, popularity et  genre.

-->Ajout de types (VARCHAR, FLOAT, BOOLEAN, INT)

-->Nettoyage SQL (suppression des chansons avec durée nulle, normalisation des données)



Bibliothèques utilisées : SQL | SQLite | Jupyter



Étape 5 – Requêtage SQL (analyse avancée) + rapports analytiques:

-->Requêtes simples : "Lister les 10 morceaux les plus populaires","Lister top genres"

-->Requêtes intermédiaires : "Répartition des morceaux par année de sortie"

-->Visualisation via Power BI



Bibliothèques utilisées : SQL | SQLite | Power BI



Résultats clés et enseignements :

--> Plus de 70% des morceaux analysés ont une popularité supérieure à 60 : des playlists très “grand public” !

--> Et surprise : certains genres très présents ne correspondent pas à ceux que je pensais écouter le plus. Comme quoi, la data ne ment pas !



Ce projet m’a permis de : 

-->Renforcer mes compétences en extraction via API, manipulation de données, visualisation, et requêtage SQL

-->Mener une analyse complète de bout en bout, du fichier brut à l’interface utilisateur

-->Découvrir l’intérêt d’un storytelling personnalisé autour de la data musicale



Maintenant, je suis curieuse :

--> Qu’est-ce que vous aimeriez apprendre sur vos playlists ?

--> Plutôt team “musique mainstream” ou “perle rare” ?



