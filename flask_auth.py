import os
import json
from datetime import datetime
from flask import Flask, redirect, request, session, jsonify
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv

# Setup Flask
app = Flask(__name__)
app.secret_key = '3f1a5e11c3a1b76fdf5824b3887391ae34'

# Load .env variables
load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = 'https://cuddly-space-lamp-wwgx45rjg7whgp49-8503.app.github.dev/callback' 

# Spotify URLs
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

# Chemin absolu pour le token
TOKEN_PATH = os.path.join(os.getcwd(), "spotify_token.json")

# Initialisation du token avec toutes les clés attendues
if not os.path.exists(TOKEN_PATH) or os.path.getsize(TOKEN_PATH) == 0:
    with open(TOKEN_PATH, "w") as f:
        json.dump({
            "access_token": "",
            "refresh_token": "",
            "expires_in": 0,
            "expires_at": 0
        }, f)

@app.route('/')
def home():
    return '''
    <h1>Bienvenue sur l'authentification Spotify</h1>
    <p><a href="/login">Clique ici pour te connecter avec Spotify</a></p>
    '''

@app.route('/login')
def login():
    # AJOUT DES SCOPES NÉCESSAIRES POUR LES AUDIO FEATURES
    scope = 'playlist-read-private user-library-read user-top-read user-read-private'
    
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    try:
        if 'error' in request.args:
            return jsonify({"error": request.args['error']})

        if 'code' in request.args:
            req_body = {
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': REDIRECT_URI,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET
            }

            response = requests.post(TOKEN_URL, data=req_body)
            token_info = response.json()

            # Stockage session Flask
            session['access_token'] = token_info['access_token']
            session['refresh_token'] = token_info.get('refresh_token')
            session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

            # Sauvegarde pour Streamlit
            with open("spotify_token.json", "w") as f:
                json.dump({
                    "access_token": token_info['access_token'],
                    "refresh_token": token_info.get('refresh_token'),
                    "expires_in": token_info['expires_in'],
                    "expires_at": session['expires_at']
                }, f)

            return redirect("https://cuddly-space-lamp-wwgx45rjg7whgp49-8501.app.github.dev/") 

        else:
            return "Code d'autorisation manquant", 400

    except Exception as e:
        return f"Erreur dans /callback : {e}", 500

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session.get('expires_at', 0):
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        if response.status_code != 200:
            return f"Erreur lors du rafraîchissement du token : {response.text}", 500

        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        try:
            with open("spotify_token.json", "r") as f:
                old_data = json.load(f)
        except FileNotFoundError:
            old_data = {}

        old_data.update({
            "access_token": new_token_info["access_token"],
            "expires_in": new_token_info["expires_in"],
            "expires_at": session["expires_at"]
        })

        with open("spotify_token.json", "w") as f:
            json.dump(old_data, f)

        return "Token rafraîchi avec succès."

    return "Token encore valide, pas besoin de rafraîchir."

if __name__ == "__main__":
    if not os.path.exists("spotify_token.json"):
        print("Token invalide : spotify_token.json introuvable; Va sur /login pour t’authentifier.")
    else:
        print("Fichier token trouvé. Lancement du serveur Flask.")
    
    app.run(port=8503)
