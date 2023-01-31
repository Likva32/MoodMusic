import base64
import datetime
import json
from urllib.parse import urlencode

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
access_token = client.access_token
header = {
    'Authorization': f'Bearer {access_token}'
}
endpoint = "https://api.spotify.com/v1/search"
data = urlencode({"q": "щенки", "type": "track"})

lookup_url = f"{endpoint}?{data}"
r = requests.get(lookup_url, headers=header)
print(r.status_code)

parsed = json.loads(r.text)
print(json.dumps(parsed, indent=4))
# method = "POST"
