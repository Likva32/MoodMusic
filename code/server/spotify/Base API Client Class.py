import base64
import datetime

import requests

client_id = '8eee557f043442a79308c93e5facc2a5'
client_secret = '310a9dbca1fb46dbafdd584ca503c2fb'


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expires = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, *args, **kwargs):
        # super.__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f'{client_id}:{client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64

    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        token_header = {
            'Authorization': f'Basic {client_creds_b64.decode()}'
        }
        return token_header

    def get_token_data(self):
        return {
            'grant_type': 'client_credentials'
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_header = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_header)
        print(r.json())
        if r.status_code not in range(200, 299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        self.access_token = access_token
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expires = expires < now
        return True


client = SpotifyAPI(client_id, client_secret)
print(client.perform_auth())
print(client.access_token)
# method = "POST"

# # Initialize the Spotify client with your client ID and client secret.py
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='your_client_id',
#                                                client_secret='your_client_secret',
#                                                redirect_uri='your_redirect_uri',
#                                                scope=['playlist-modify-public', 'playlist-modify-private'],
#                                                cache_path='.spotipyoauthcache'))
#
# # Create a new playlist
# playlist_name = 'My New Playlist'
# playlist_description = 'A playlist of my favorite songs'
# playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, description=playlist_description)
#
# # Get the ID of the new playlist
# playlist_id = playlist['id']
#
# # Search for tracks to add to the playlist
# tracks = sp.search(q='artist:The Beatles', type='track')['tracks']['items']
#
# # Add the tracks to the playlist
# track_uris = [track['uri'] for track in tracks]
# sp.playlist_add_items(playlist_id, track_uris)
