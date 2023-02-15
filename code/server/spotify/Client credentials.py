import base64
import datetime
import json
from urllib.parse import urlencode

import requests

client_id = '8eee557f043442a79308c93e5facc2a5'
client_secret = '679227b6e0e3405eb972048fd79f83a7'


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
            raise Exception('Authentication failed')
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        self.access_token = access_token
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expires = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token is None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        header = {
            'Authorization': f'Bearer {access_token}'
        }
        return header

    def get_resource(self, lookup_id, resource_type='artists', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        header = self.get_resource_header()
        r = requests.get(url=endpoint, headers=header)
        print(r.status_code)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def save_album(self, id):
        endpoint = f"https://api.spotify.com/v1/me"
        header = self.get_resource_header()
        r = requests.get(url=endpoint, headers=header)
        print(r.status_code)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def base_search(self, query_params):
        header = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=header)
        print(r.status_code)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def search(self, query=None, operator=None, operator_query=None, search_type='album'):
        if query is None:
            raise Exception('A query is required')
        if isinstance(query, dict):
            query = ' '.join([f"{k}:{v}" for k, v in query.items()])
        if operator is not None and operator_query is not None:
            if operator.lower() == 'or' or operator_query.lower() == 'not':
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        return self.base_search(query_params)


client = SpotifyAPI(client_id, client_secret)
track = client.search({'track': 'хочу перемен'}, search_type='track')

track = client.search({'album': 'Третья жизнь'}, search_type='album')
x = client.get_album('2LVpEKk26LDKoEV5aZipL5')

print(json.dumps(track, indent=4))

# artist = client.get_artist('2jkl2xJVm71azWAgZKyf42')
# print(json.dumps(artist, indent=4))
# method = "POST"
# print(artist["name"])

# save = client.save_album('twvqi8x7hozsqphmrezr70cmn?si=e0b8dca6babd4ec0')
# print(json.dumps(save, indent=4))
