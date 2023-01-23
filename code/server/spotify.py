import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize the Spotify client with your client ID and client secret
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='your_client_id',
                                               client_secret='your_client_secret',
                                               redirect_uri='your_redirect_uri',
                                               scope=['playlist-modify-public','playlist-modify-private'],
                                               cache_path='.spotipyoauthcache'))

# Create a new playlist
playlist_name = 'My New Playlist'
playlist_description = 'A playlist of my favorite songs'
playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, description=playlist_description)

# Get the ID of the new playlist
playlist_id = playlist['id']

# Search for tracks to add to the playlist
tracks = sp.search(q='artist:The Beatles', type='track')['tracks']['items']

# Add the tracks to the playlist
track_uris = [track['uri'] for track in tracks]
sp.playlist_add_items(playlist_id, track_uris)
