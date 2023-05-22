"""
    Module Name: SpotifyFunc

    Description:
        This module provides functionality for handling Spotify API, including obtaining and refreshing tokens,
        interacting with the Spotify API, and creating playlists based on mood.

    Dependencies:
        - json
        - time
        - spotipy
        - loguru.logger
        - spotipy.oauth2.SpotifyOAuth
        - DataBase.Users.Users
        - lib.secret.client_id
        - lib.secret.client_secret

    Classes:
        - MySpotifyFunc: A class for handling Spotify functionality.

    Author: Artur Tkach (Likva32 on GitHub)
"""

import json
import time

import spotipy
from loguru import logger
from spotipy.oauth2 import SpotifyOAuth

from DataBase.Users import Users
from lib.secret import client_id, client_secret


class MySpotifyFunc:
    """
        A class for handling Spotify functionality, such as obtaining and refreshing tokens,
        interacting with the Spotify API, and creating playlists based on mood.

        Attributes:
            - Email (str): The email address associated with the user.
            - UsersDb (DataBase.Users.Users): An instance of the Users class for user database operations.
            - token_info (dict): A dictionary containing the token information.

        Methods:
            - __init__(Email): Initializes the MySpotifyFunc class with the specified email address.
            - get_token(): Checks if the token is valid and gets a new token if necessary.
            - get_current_user(): Retrieves information about the current user.
            - create_playlist(mood): Creates a new playlist based on the specified mood.
            - create_spotify_oauth():  Creates a SpotifyOAuth object for authorization.

    """
    def __init__(self, Email):
        """
            Initializes the MySpotifyFunc class with the specified email address.

            Parameters:
                Email (str): The email address associated with the user.
        """
        self.Email = Email
        self.UsersDb = Users()
        self.token_info = json.loads(self.UsersDb.get_token(self.Email))

    # Checks to see if token is valid and gets a new token if not
    def get_token(self):
        """
            Checks if the token is valid and gets a new token if necessary.

            Returns:
                tuple: A tuple containing the token information and a flag indicating if the token is valid.
        """
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
        """
            Retrieves information about the current user.

            Returns:
                str: A JSON-encoded string containing the current user's information.
        """
        self.token_info, authorized = self.get_token()
        if not authorized:
            logger.error("error, u need to re-login to spotify again")
            return "bad"
        sp = spotipy.Spotify(auth=self.token_info['access_token'])
        user = sp.current_user()
        return json.dumps(user)

    def create_playlist(self, mood):
        """
            Creates a new playlist based on the specified mood.

            Parameters:
                mood (str): The mood for which the playlist should be created.
            Returns:
                str: A message indicating the success or failure of the playlist creation.
        """
        self.token_info, authorized = self.get_token()
        logger.debug(authorized)
        if not authorized:
            logger.error("error, u need to re-login to spotify again")
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
        """
            Creates a SpotifyOAuth object for authorization.

            Returns:
                spotipy.oauth2.SpotifyOAuth: A SpotifyOAuth object.
        """
        return SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri='http://127.0.0.1:5000/',
            scope="user-library-read")
