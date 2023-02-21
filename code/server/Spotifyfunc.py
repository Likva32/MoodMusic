import json
import time

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from DataBase.Users import Users
from lib.secret import client_id, client_secret


# App config
class MySpotifyFunc:
    def __init__(self, Email):
        self.Email = Email
        self.UsersDb = Users()
        self.token_info = json.loads(self.UsersDb.get_token(self.Email))

    def get_all_tracks(self):
        self.token_info, authorized = self.get_token()
        print('----------')
        print(authorized)
        if not authorized:
            print("error, u need to re-login to spotify again")
            return "bad"
            # raise "error, u need to re-login to spotify again"
            # pass  go to login
        sp = spotipy.Spotify(auth=self.token_info['access_token'])
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
        token_info = self.token_info

        # Checking if the session already has a token stored
        if not self.token_info:
            token_valid = False
            return token_info, token_valid

        # Checking if token has expired
        now = int(time.time())
        is_token_expired = self.token_info['expires_at'] - now < 60

        # Refreshing token if it has expired
        if is_token_expired:
            sp_oauth = self.create_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(self.token_info['refresh_token'])

        token_valid = True
        return token_info, token_valid

    def get_current_user(self):
        self.token_info, authorized = self.get_token()
        if not authorized:
            print("error, u need to re-login to spotify again")
            return "bad"
        sp = spotipy.Spotify(auth=self.token_info['access_token'])
        user = sp.current_user()
        print(user)
        return json.dumps(user)

    def create_spotify_oauth(self):
        return SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri='http://127.0.0.1:5000/',
            scope="user-library-read")
