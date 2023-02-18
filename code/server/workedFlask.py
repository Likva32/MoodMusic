import json
import time

import pandas as pd
import spotipy
from flask import Flask, url_for, session, request, redirect, render_template
from spotipy.oauth2 import SpotifyOAuth

from DataBase.Users import Users
from lib.secretsId import client_id, client_secret


# App config
class MyFlaskApp:
    def __init__(self, name, Email):
        self.app = Flask(name)
        self.Email = Email
        self.UsersDb = Users()
        self.app.secret_key = 'SOMETHING-RANDOM'
        self.app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

        @self.app.route('/')
        def login():
            sp_oauth = self.create_spotify_oauth()
            auth_url = sp_oauth.get_authorize_url()
            print(auth_url)
            return redirect(auth_url)

        @self.app.route('/authorize')
        def authorize():
            sp_oauth = self.create_spotify_oauth()
            session.clear()
            code = request.args.get('code')
            if not code:
                return redirect(url_for('login', _external=True))
            token_info = sp_oauth.get_access_token(code)
            print('blabla')
            print(token_info)
            print('blabla')
            session["token_info"] = token_info
            # return redirect("/getTracks")
            self.UsersDb.insert_token(self.Email, json.dumps(token_info))
            print('good')
            return render_template('main.html')

        @self.app.route('/logout')
        def logout():
            for key in list(session.keys()):
                session.pop(key)
            return redirect('/')

        @self.app.route('/getTracks')
        def get_all_tracks():
            session['token_info'], authorized = self.get_token()
            print('----------')
            print(authorized)
            session.modified = True
            if not authorized:
                return redirect(url_for('login', _external=True))
            sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
            results = []
            iter = 0
            while True:
                offset = iter * 50
                iter += 1
                curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
                for idx, item in enumerate(curGroup):
                    track = item['track']
                    val = track['name'] + " - " + track['artists'][0]['name']
                    results += [val]
                if len(curGroup) < 50:
                    break

            df = pd.DataFrame(results, columns=["song names"])
            df.to_csv('songs.csv', index=False)
            return "done"

    # Checks to see if token is valid and gets a new token if not
    def get_token(self):
        token_valid = False
        token_info = session.get("token_info", {})

        # Checking if the session already has a token stored
        if not (session.get('token_info', False)):
            token_valid = False
            return token_info, token_valid

        # Checking if token has expired
        now = int(time.time())
        is_token_expired = session.get('token_info').get('expires_at') - now < 60

        # Refreshing token if it has expired
        if is_token_expired:
            sp_oauth = self.create_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

        token_valid = True
        return token_info, token_valid

    def create_spotify_oauth(self):
        return SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=url_for('authorize', _external=True),
            scope="user-library-read")

    def run(self):
        self.app.run()

# app.run(debug=True)
