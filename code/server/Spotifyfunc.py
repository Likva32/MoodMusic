import json
import time

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

    def create_playlist(self, mood):
        self.token_info, authorized = self.get_token()
        print('----------')
        print(authorized)
        if not authorized:
            print("error, u need to re-login to spotify again")
            return "bad"
            # raise "error, u need to re-login to spotify again"
            # pass  go to login
        scope = "playlist-modify-public"
        sp = spotipy.Spotify(auth=self.token_info['access_token'])

        # Create a new playlist

        if not mood:
            mood = 'Neutral'
        genre_dict = {
            'Angry': 'Heavy Metal',
            'Disgust': 'Experimental',
            'Fear': 'Horrorcore',
            'Happy': 'Electronic',
            'Sad': 'Blues',
            'Surprise': 'Jazz',
            'Neutral': 'Ambient'
        }
        genre = genre_dict[mood]
        playlist_name = f"{mood} Playlist by MoodMusic"
        playlist_description = "This is my new playlist"
        user_id = sp.current_user()["id"]
        # playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, description=playlist_description)
        playlists = sp.user_playlists(sp.me()['id'])
        playlist = None
        for pl in playlists['items']:
            if pl['name'] == playlist_name:
                playlist = pl
                break
        if not playlist:
            playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, description=playlist_description)
        search_query = f"genre:{genre}"  # mood
        results = sp.search(q=search_query, type='track', limit=50)

        tracks = [item['uri'] for item in results['tracks']['items']]
        if tracks:
            sp.playlist_add_items(playlist_id=playlist['id'], items=tracks)
            return f"Added {len(tracks)} {mood} songs to '{playlist_name}'!"
        else:
            return f"No {mood} songs found on Spotify."

    def create_spotify_oauth(self):
        return SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri='http://127.0.0.1:5000/',
            scope="user-library-read")
