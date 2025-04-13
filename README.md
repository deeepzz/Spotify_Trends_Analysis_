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
