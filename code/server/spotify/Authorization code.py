import base64
import datetime
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse

import requests

client_id = '8eee557f043442a79308c93e5facc2a5'
client_secret = '679227b6e0e3405eb972048fd79f83a7'


class SpotifyAPI:
    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    API_BASE_URL = "https://api.spotify.com/v1"
    access_token = None
    access_token_expires_at = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expires = True
    client_id = None
    client_secret = None

    def __init__(self, client_id, client_secret, redirect_uri, *args, **kwargs):
        # super.__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self, state, scope):
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "state": state,
            "scope": scope
        }
        authorization_url = f"{self.AUTH_URL}?{urlencode(params)}"
        return authorization_url

    def get_access_token(self, code):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}"
        }
        data = {
            "grant_type": "authorization_code",
            "response_type": code,
            "redirect_uri": self.redirect_uri
        }
        response = requests.post(self.TOKEN_URL, headers=headers, data=data)
        response_json = response.json()
        access_token = response_json.get("access_token")
        return access_token

    def get_current_user(self, access_token):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(f"{self.API_BASE_URL}/me", headers=headers)
        response_json = response.json()
        return response_json

    def get_user_playlists(self, access_token, user_id):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(f"{self.API_BASE_URL}/users/{user_id}/playlists", headers=headers)
        response_json = response.json()
        return response_json

    def get_playlist_tracks(self, access_token, playlist_id):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(f"{self.API_BASE_URL}/playlists/{playlist_id}/tracks", headers=headers)
        response_json = response.json()
        return response_json


# Initialize the SpotifyAPI object with your client ID, client secret, and redirect URI
spotify = SpotifyAPI(client_id, client_secret, 'https://www.google.com/')

# Get the authorization URL for the user to grant access
state = ""
scope = "user-library-read user-library-modify playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"
authorization_url = spotify.get_authorization_url(state, scope)
print(authorization_url)
parsed_url = urlparse(
    'https://www.google.com/?code=AQCctbS6PzP6gEuLgodttBRewtIKB8SgRpzcrsI-Z8x8ll6HEDiuH-8k-vbqahSctHKWw-HS7eoEq61BVeSstyf16WZrLwAQ-q7oRiW0C5U-OIW32yEVb5DzLld0TswWdhf7vQRpj73DhShTeQaFCF5khOgdv9BQ_tXU95B1vf61D6bh7b40o036WG9dIScRPJGce-7CP9MtsDL7d2Xbo3iYXsvgJ-wV4QVO8GsZb2nEGwsG-x9Z8iiLV2iYgSeK2-L6DVq60v6wRI386X_ix93sEh4zOVmBfEBc1nE8l97vrDQLyXcqdioJU8vsppocpomWIWRGl5kD6cyiEXFHM61xS15j1qqL&state=israel')
captured_value = parse_qs(parsed_url.query)['code'][0]
code = captured_value
print(captured_value)
# After the user grants access, they will be redirected to the redirect URI with a code in the query parameters
# Extract the code from the query parameters and use it to get the access token
access_token = spotify.get_access_token(code)
print(access_token)
# # Use the access token to get information about the current user
# current_user = spotify.get_current_user(access_token)
# print(json.dumps(current_user, indent=4))
# Use the access token to get the user's playlists


# playlists = spotify.get_user_playlists(access_token, current_user["id"])


# Use the access token to get the tracks of a specific playlist


# playlist_id = "the_id_of_the_playlist"
# tracks = spotify.get_playlist_tracks(access_token, playlist_id)


# Use the access token to create a new playlist
# new_playlist_name = "My New Playlist"
# new_playlist_description = "This is a description of my new playlist"
# spotify.create_playlist(access_token, current_user["id"], new_playlist_name, new_playlist_description)
