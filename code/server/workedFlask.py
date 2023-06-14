"""
    Module Name: workedFlask

    Description:
        This module provides functionality for a Flask application that handles Spotify login and authorization.

    Dependencies:
        - hashlib
        - json
        - time
        - spotipy
        - flask.Flask
        - flask.url_for
        - flask.session
        - flask.request
        - flask.redirect
        - flask.render_template
        - loguru.logger
        - spotipy.oauth2.SpotifyOAuth
        - DataBase.Users.Users
        - lib.secret.client_id
        - lib.secret.client_secret
        - lib.secret.secret_key

    Classes:
        - MyFlaskApp: A class for a Flask application that handles Spotify login and authorization.

    Author: Artur Tkach (Likva32 on GitHub)
"""
import hashlib
import json
import time

import spotipy
from flask import Flask, url_for, session, request, redirect, render_template
from loguru import logger
from spotipy.oauth2 import SpotifyOAuth

from DataBase.Users import Users
from lib.secret import client_id, client_secret
from lib.secret import secret_key


class MyFlaskApp:
    """
        A class for a Flask application that handles Spotify login and authorization.

        Attributes:
            app (flask.Flask): The Flask application.
            UsersDb (DataBase.Users.Users): An instance of the Users class for user database operations.

        Methods:
            __init__(name): Initializes the MyFlaskApp class with the specified name.
            appLogin(): Handles the login page route and login functionality.
            login(): Handles the login route and redirects to the Spotify authorization page.
            authorize(): Handles the authorization route and retrieves the Spotify access token.
            get_token(): Checks if the token is valid and gets a new token if necessary.
            get_current_user(token_info): Retrieves information about the current user.
            create_spotify_oauth(): Creates a SpotifyOAuth object for authorization.
            run(ip): Runs the Flask application.

        """

    def __init__(self, name):
        """
            Initializes the MyFlaskApp class with the specified name.

            Parameters:
                name (str): The name of the Flask application.
        """
        self.app = Flask(name, static_url_path='/static')
        self.UsersDb = Users()
        self.app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'
        # self.app.config['EMAIL'] = 'email'
        self.app.config['SESSION_TYPE'] = 'filesystem'
        self.app.config['SECRET_KEY'] = "Shhh..ItsASecret"
        self.app.secret_key = secret_key  # random string to encrypt the session

        @self.app.route('/', methods=["POST", "GET"])
        def appLogin():
            """
                Handles the login page route and login functionality.
            """
            msg = ''
            if request.method == "POST":
                email = request.form["email"]
                session["email"] = email
                password = request.form["password"]
                session["password"] = password

                salt = 'MoodMusic'
                hashed_pass = hashlib.md5(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()

                if self.UsersDb.Login(email, hashed_pass):
                    logger.success('Login success (Flask)')
                    return redirect('/log')
                else:
                    logger.error('Login NOT success (Flask)')
                    msg = 'Wrong Password or Email'
                    return render_template('email_form.html', msg=msg)
            return render_template('email_form.html', msg=msg)

        @self.app.route('/log')
        def login():
            """
                Handles the login route and redirects to the Spotify authorization page.
            """
            # session['email'] = self.Email
            sp_oauth = self.create_spotify_oauth()
            auth_url = sp_oauth.get_authorize_url()
            return redirect(auth_url)

        @self.app.route('/authorize')
        def authorize():
            """
                Handles the authorization route and retrieves the Spotify access token.
            """
            sp_oauth = self.create_spotify_oauth()
            # session.clear()
            if session.get('token_info'):
                session.pop('token_info')
            code = request.args.get('code')
            if not code:
                return redirect(url_for('login', _external=True))
            token_info = sp_oauth.get_access_token(code)
            session["token_info"] = token_info

            user = self.get_current_user(token_info)
            user = json.loads(user)
            url = user["external_urls"]["spotify"]

            email = session.get('email')

            status, description = self.UsersDb.url_exist(email, url, json.dumps(token_info))
            return render_template('main.html', status=status, description=description)

    # Checks to see if token is valid and gets a new token if not
    def get_token(self):
        """
            Checks if the token is valid and gets a new token if necessary.

            Returns:
                tuple: A tuple containing the token information and a flag indicating if the token is valid.
        """
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

    def get_current_user(self, token_info):
        """
            Retrieves information about the current user.

            Parameters:
                token_info (dict): A dictionary containing the token information.
            Returns:
                str: A JSON-encoded string containing the current user's information.
        """
        token_info, authorized = self.get_token()
        if not authorized:
            logger.error("error, u need to re-login to spotify again (Flask)")
            return "bad"
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user = sp.current_user()
        return json.dumps(user)

    def create_spotify_oauth(self):
        """
            Creates a SpotifyOAuth object for authorization.

            Returns:
                spotipy.oauth2.SpotifyOAuth: A SpotifyOAuth object.
        """
        return SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=url_for('authorize', _external=True),
            scope="user-library-read")

    def run(self, ip):
        """
            Runs the Flask application.

            Parameters:
                ip (str): The IP address on which to run the application.
        """
        self.app.run(host=ip)

# app.run(debug=True)
